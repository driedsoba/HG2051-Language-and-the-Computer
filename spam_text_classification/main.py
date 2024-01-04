## Names and Matric Numbers:
# Choo Shuen Ming U1931232D
# Daniel Kainovan Handoyo U2230837E
# Liw Jun Le U2221922D

import pandas as pd
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from src.data_processing import load_data, preprocess_text
from src.feature_engineering import extract_features
from src.model import train_model, evaluate_model, cross_validate_model
from src.utils import write_metrics_to_file, print_metrics

use_grid_search = True

# Load and preprocess smsdatacollection
sms_data = load_data('datasets/SMSSpamCollection.txt')
sms_data['message'] = [preprocess_text(text) for text in tqdm(sms_data['message'], desc="Preprocessing SMS Data")]

# Split the smsdatacollection into training set
train_df, _ = train_test_split(sms_data, test_size=0.2, random_state=42, stratify=sms_data['label'])

# Load and preprocess lingspam_data
lingspam_data = load_data('datasets/email_corpus_lingspam.txt')
lingspam_data['message'] = [preprocess_text(text) for text in tqdm(lingspam_data['message'], desc="Preprocessing LingSpam Data")]

# Use the entire lingspam_data as test set
test_df = lingspam_data

# Feature extraction
X_train, y_train, vectorizer = extract_features(train_df)

# Train the model with grid search
model = train_model(X_train, y_train, use_grid_search=use_grid_search)

# Cross-validation
cv_results = cross_validate_model(X_train, y_train)

# Feature extraction for the test set
X_test, y_test, _ = extract_features(test_df, vectorizer=vectorizer)

# Evaluate the model on the test set
test_metrics = evaluate_model(model, X_test, y_test)

# Write metrics to output file
write_metrics_to_file(cv_results, 'output.txt', test_metrics)
print_metrics(cv_results, test_metrics)

# #Confusion matrix plotting

# from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
# import matplotlib.pyplot as plt
# # Plot non-normalized confusion matrix
# titles_options = [
#     ("Confusion matrix, without normalization", None),
#     ("Normalized confusion matrix", "true"),
# ]
# for title, normalize in titles_options:
#     disp = ConfusionMatrixDisplay.from_estimator(
#         model,
#         X_test,
#         y_test,
#         display_labels= model.classes_,
#         cmap=plt.cm.Blues,
#         normalize=normalize,
#     )
#     disp.ax_.set_title(title)

#     print(title)
#     print(disp.confusion_matrix)

# plt.show()
