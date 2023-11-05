# Financial Sentiment Analysis 

#### Created by Andrew McLaughlin and Jack Hastings

## Introduction 


## Contents of Repository

## Cleaning and EDA


In the folder “original_data” there are 6 csv’s containing most of the data used in this project. The following lists the name of the csv file and its source,

-	companies_1.csv - https://www.kaggle.com/datasets/sbhatti/financial-sentiment-analysis/data
-	SEntFiN-v1.1.csv - https://www.kaggle.com/datasets/ankurzing/aspect-based-sentiment-analysis-for-financial-news
-	phrasebook.csv - https://huggingface.co/datasets/financial_phrasebank
-	stock_news.csv - https://www.kaggle.com/datasets/johoetter/labeled-stock-news-headlines
-	sent_train.csv and sent_valid.csv - https://huggingface.co/datasets/zeroshot/twitter-financial-news-sentiment/viewer/default/train

There is also an excel file called negative_guardian.xlsx which was the result of manually searching through negative_guardian.csv (located in the folder guardian_negative) in excel and removing headlines that were not negative. The file negative_guardian.csv itself was created from the notebook guardian_negative.ipynb using the csv guardian_headlines.csv (both located in the folder guardian_negative). The way that negative_guardian.xlsx was created can be seen in the notebook but was determined to be a slow and ineffective way of creating our own data set and so was abandoned, however about 2500 negative headlines were found through this method and were used to train and validate the neural network. 

The original data set containing guardian_headlines.csv can be found here:https://www.kaggle.com/datasets/notlucasp/financial-news-headlines

The excel file words, which contains a list of words with negative and positive connotations can be found here: https://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html

In the notebook Pre-processing.ipynb, these 7 data sets were combined and cleaned. Cleaning involved removal of URLs, removal of irrelevant strings such as “UPDATE –” and “Politics live with Andrew Sparrow” along with non-alphanumeric characters such as commas, apostrophes etc. The reason we removed non-alphanumeric characters was that the tokenizer (spoken about in the next section in more depth) used to create the neural network would treat two strings for example ‘meltdown’ and meltdown as two different tokens because of the apostrophes, however, we wanted all occurrences of the same word to be picked up by the NN. We also removed strings such as “US” and “UK” since they occurred frequently, and it was a possibility that the NN would associate them more heavily with either negative or positive sentiments depending on the training data, i.e., if there were particular strings such as the ones mentioned above that occurred more in negative headlines then upon seeing them the NN would be biased towards negative, especially if the NN was not familiar with the other words in the string. 



## The Neural Network

## The Webpage

## Instructions on Running the Webpage

## Acknowledgements 
