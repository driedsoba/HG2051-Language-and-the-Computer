[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/V9O7PxYS)
# HG2051 (AY23/24) Project 2: Group assignment

This project develops a machine learning classifier to distinguish between spam and non-spam (ham) textual data. 
It uses Natural Language Processing (NLP) to preprocess text data from email and SMS sources, 
applies Naive Bayes, SVM, and logistic regression classification algorithms, and evaluates the model's performance using various metrics.

## Project Setup
Install the required packages by running the following command in your terminal:
```bash
pip install -r requirements.txt
```

The following scripts are included in this directory:
- `main.py`: trains a model using multinomial Naive Bayes classifier with SMS dataset. The module is evaluated with cross-validation and 
the Lingspam dataset. The script generates metrics and outputs the results to a file `output.txt`.
- `logisticregression.py`: trains a model using logistic regression classifier with SMS dataset. The module is evaluated with cross-validation and 
the Lingspam dataset. The script generates metrics and outputs the results to a file `lr_output.txt`.
- `svm.py`: trains a model using SVM classifier with SMS dataset. The module is evaluated with cross-validation and 
the Lingspam dataset. The script generates metrics and outputs the results to a file `svm_output.txt`.

The following folders are used to store the files and functions used for processing:
- `datasets` contains the SMS spam collection and Lingspam corpus datasets
- `logisticregression` contains the output metrics of the logisticregression classifier
- `svm` contains the output metrics of the SVM classifier
- `src` contains the data processing, EDA, feature engineering, model and utils functions
