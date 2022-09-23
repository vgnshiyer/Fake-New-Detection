import pickle
from flask import Flask, jsonify    
from flask_cors import CORS, cross_origin
import pandas as pd
import nltk
from nltk.corpus import stopwords
import re
import numpy as np
import json
from statistics import mean
from collections import Counter
from time import sleep

from sklearn.feature_extraction.text import CountVectorizer ##Bow model
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer  ## TFIDF Model
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
from scipy import sparse
from sklearn.externals import joblib
import xgboost

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

app = Flask(__name__)
CORS(app)

@app.route('/')
def cleanhtml(sentence):
    cleanr=re.compile('<.*?>')
    cleantext=re.sub(cleanr,' ',sentence)
    return cleantext

@app.route('/')
def cleanpunc(sentence):
    '''This function cleans all the punctuation or special characters from a given sentence'''
    cleaned = re.sub(r'[?|@|!|^|%|\'|"|#]',r'',sentence)
    cleaned = re.sub(r'[.|,|)|(|\|/]',r' ',cleaned)
    return  cleaned

@app.route('/')
def calc_avg_w2v(list_of_sent, w2v_model):
    
      ## Initialize an empty list
    sent_vectors = []
    ## Consider one sentence/review at a time
    for sent in list_of_sent:
        ## Initialize sentence vector to 0
        sent_vec = np.zeros(300)
        ## Initialize count of words to 0
        cnt_words = 0
        ## Consider the words one by one
        for word in sent:
            try:
                ## Calculate the word vector using the W2V model
                vec = w2v_model[word]
                ## Add the word vector to the sentence vector (This is the numerator)
                sent_vec += vec
                ## Sum all the word counts (This is the denominator)
                cnt_words += 1
            except:
                pass
        ## Divide the numerator by the denominator to get the sentence vector
        sent_vec /= cnt_words
        ## Add the sentence vector in the final list
        sent_vectors.append(sent_vec)
    ## return the list of all the sentence vectors
    return sent_vectors

@app.route('/')
def preprocessing(series):

    stop=set(stopwords.words('english'))
    sno=nltk.stem.SnowballStemmer('english')
    i=0
    str1=" "
    final_string=[]
    list_of_sent=[]
    
    for sent in series.values:
        filtered_sent=[]
        sent=cleanhtml(sent)
        sent=cleanpunc(sent)
        for cleaned_words in sent.split():
             if((cleaned_words.isalpha()) & (len(cleaned_words) > 2)):
                    if(cleaned_words.lower() not in stop):
                        s = (sno.stem(cleaned_words.lower()))
                        filtered_sent.append(s)    
        list_of_sent.append(filtered_sent)
        str1 = " ".join(filtered_sent)
        final_string.append(str1)
        i += 1
    return final_string, list_of_sent

@app.route('/')
def compute_sentiment(sentences):
    #calculate the polarity score of each sentence then take the average
    sid = SentimentIntensityAnalyzer()
    result = []
    for sentence in sentences:
        vs = sid.polarity_scores(sentence)
        result.append(vs)
    return pd.DataFrame(result).mean()

@app.route("/checknews/<var>", methods=["GET"])
def detecting_fake_news(var):

    #loading the web crawler
    sample_headline=[]
    stances=[]
    driver = webdriver.Chrome("chromedriver.exe")
    # driver.set_window_position(-10000,0)
    #l=['Britain’s House of Commons reconvened on September 25, a day after the bombshell Supreme Court ruling that Prime Minister Boris Johnson had acted illegally by suspending Parliament, and lawmakers immediately demanded answers about how the suspension came about in the first place.']


    #loading the model
    model = joblib.load('XGB_10000.pkl')

    sample_body=str(var)
    #print(var)

    #scraping headlines from google news
    driver.get('http://google.com')
    search = driver.find_element_by_name("q")
    search.clear()
    search.send_keys(sample_body)
    search.send_keys(Keys.RETURN) # hit return after you enter search text
    hrefs=[]
    src=[]
    tab=driver.find_elements_by_css_selector('div.hdtb-mitem')
    print(tab)
    for i in range(0,5):
        if tab[i].text == 'News':
            print(tab[i].text)
            tab[i].click()
            break
    else:
        #code for saying invalid input
        res= -1
        return str(res)
    # driver.find_element_by_xpath('//*[@id="hdtb-msb-vis"]/div[2]/a').click()
    sleep(1)
    #finding top 7 results
    for j in range(0,11):
        try:
            results = driver.find_elements_by_css_selector('div.gG0TJc')
            link = results[j].find_element_by_tag_name("h3")
            #print(link.text)
            href = results[j].find_element_by_tag_name("a").get_attribute("href")
            a=driver.find_element_by_xpath('/html/body/div[6]/div[3]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div/div['+str(j+1)+']/div/a/img')
            src.append(a.get_attribute('src'))
            sample_headline.append(link.text)
            hrefs.append(href)

        except:
            pass
    # images = driver.find_elements_by_css_selector('img.th')
    # for image in images:
    #     src.append(image.get_attribute('src'))

    #loading pickle files
    with open('vocab_tfidf.pkl','rb') as pickle_file:
        vocabulary=pickle.load(pickle_file)
    with open('vocab_bow.pkl','rb') as pickle_file:
        vocabulary1=pickle.load(pickle_file)

    #Loading the google word2vec model
    with open('google_word2vec_model','rb') as pickle_file:
        google_w2v=pickle.load(pickle_file)

    c=0
    desc=sample_headline
    for sample_headline in sample_headline:
        sample_body,list_of_bodies=preprocessing(pd.DataFrame([sample_body],columns=['body'])['body'])
        sample_headline,list_of_headlines=preprocessing(pd.DataFrame([sample_headline],columns=['headline'])['headline'])

        #feature generation
        vec = TfidfVectorizer(vocabulary=vocabulary)
        sample_body_tfidf=vec.fit_transform(sample_body)
        sample_head_tfidf=vec.fit_transform(sample_headline)

        vec1 = CountVectorizer(vocabulary=vocabulary1)
        sample_body_bow=vec.fit_transform(sample_body)
        sample_head_bow=vec.fit_transform(sample_headline)

        simtfidf=cosine_similarity(sample_head_tfidf,sample_body_tfidf)
        simbow=cosine_similarity(sample_head_bow,sample_body_bow)

        body_sents=pd.DataFrame(sample_body,columns=['data'])['data'].apply(lambda x: sent_tokenize(x)).apply(lambda x: compute_sentiment(x))
        head_sents=pd.DataFrame(sample_headline,columns=['data'])['data'].apply(lambda x: sent_tokenize(x)).apply(lambda x: compute_sentiment(x))
        print(body_sents.shape)
        print(head_sents.shape)
        
        w2v_body = calc_avg_w2v(list_of_bodies,google_w2v)
        w2v_head = calc_avg_w2v(list_of_headlines,google_w2v)

        w2v_body=np.nan_to_num(np.asarray(w2v_body))
        w2v_head=np.nan_to_num(np.asarray(w2v_head))

        simw2v=cosine_similarity(w2v_body,w2v_head)

        simtfidf=sparse.csr_matrix(simtfidf)
        simbow=sparse.csr_matrix(simbow)
        simw2v=sparse.csr_matrix(simw2v)
        head_sents=sparse.csr_matrix(head_sents)
        body_sents=sparse.csr_matrix(body_sents)
        w2v_head=sparse.csr_matrix(w2v_head)
        w2v_body=sparse.csr_matrix(w2v_body)

        #dixit is good boy
        # dixit is bad boy

        X=sparse.hstack([simtfidf,simbow,head_sents,body_sents,w2v_head,w2v_body,simw2v])
        print(X.shape)
        try:
            result = model.predict(X)[0]
        except:
            pass
        stances.append(result)
        if result == 0 or result == 2:
            a_dict ={

                "img": src[c],
                "description": desc[c],
                "url": hrefs[c]
            }
            try:
                with open('../front-end/src/assets/data.json','r') as f:
                    data = json.load(f)
                data.append(a_dict)
                with open('../front-end/src/assets/data.json', 'w') as f:
                    json.dump(data, f,indent=4)
            except:
                a_dict =[{
                "img": src[c],
                "description": desc[c],
                "url": hrefs[c]
                }]
                with open('../front-end/src/assets/data.json', 'w') as f:
                    json.dump(a_dict, f,indent=4)
        c+=1
    print(hrefs)
    # print(stances)
    #if no result found
    if(len(stances)==0):
        res = 3
        return str(res)

    no_of_related_articles=0
    # counting the number of articles who confirm that the news conent as related
    if Counter(stances)[0]>0:
        no_of_related_articles=no_of_related_articles+Counter(stances)[0]
    if Counter(stances)[2]>5:
        no_of_related_articles=no_of_related_articles+Counter(stances)[2]
    
    # if the value of related articles are greater than a threshold value, then the news content is real
    if no_of_related_articles>4:
        res=0
    else:
        res=3
    return str(res)



if __name__ == "__main__":
    app.run(debug=True)