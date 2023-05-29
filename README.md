# Fake News Detection

This project is a machine learning model that can be used to detect fake news. The model is trained on a dataset of over 40,000 news articles, and it uses the XGBoost algorithm to classify articles as either fake or real.

## Features
-   Check veracity of a news article
-   View latest news update
-   Authenticate users with username and password
-   Search for news articles
-   Archive news article to view later.

**Getting Started**

To get started with Blogger, you will need to have the following installed:
-   Python 3+
-   Flask
-   Angular6
-   npm

Once you have all of the required dependencies installed, you can clone the repository from GitHub:
```
git clone https://github.com/vgnshiyer/Fake-News-Detection.git
cd Fake-News-Detection
```

Build and run the backend using
```
cd main-app && python3 app.py
```
Build and run the frontend using npm
```
cd front-end/ && npm start
```

Open [http://localhost:4200](http://localhost:4200) to view it in your browser.

**Usage:**
To use the model, simply enter a news article headline and news article body into the input fields and press enter. The application compares the article with relevant articles across the internet and uses the Machine learning model trained to classify the input article as Fake or Real. 

The model also provides probability of truth associated with each classification. This probability can be used to make more informed decisions about the veracity of the news article.
