# utils.py

import numpy as np

def write_metrics_to_file(cv_results, filename, lingspam_metrics):
    try:
        with open(filename, 'w') as f:
            for i in range(len(cv_results['test_accuracy'])):
                f.write(f"Iteration {i+1}:\n")
                f.write(f"Accuracy: {cv_results['test_accuracy'][i]}\n")
                f.write(f"Precision: {cv_results['test_precision'][i]}\n")
                f.write(f"Recall: {cv_results['test_recall'][i]}\n")
                f.write(f"F1-score: {cv_results['test_f1'][i]}\n\n")
            f.write("Average Metrics:\n")
            f.write(f"Average Accuracy: {np.mean(cv_results['test_accuracy'])}\n")
            f.write(f"Average Precision: {np.mean(cv_results['test_precision'])}\n")
            f.write(f"Average Recall: {np.mean(cv_results['test_recall'])}\n")
            f.write(f"Average F1 Score: {np.mean(cv_results['test_f1'])}\n\n")
            f.write("Lingspam Data Evaluation Metrics:\n")
            f.write(f"Accuracy: {lingspam_metrics['accuracy']}\n")
            f.write(f"Precision: {lingspam_metrics['precision']}\n")
            f.write(f"Recall: {lingspam_metrics['recall']}\n")
            f.write(f"F1 Score: {lingspam_metrics['f1']}\n")
    except Exception as e:
        print(f"Error writing to file: {e}")

def print_metrics(cv_results, lingspam_metrics):
    print("\nCross-Validation Metrics:")
    for i in range(len(cv_results['test_accuracy'])):
        print(f"Iteration {i+1}:")
        print(f"Accuracy: {cv_results['test_accuracy'][i]}")
        print(f"Precision: {cv_results['test_precision'][i]}")
        print(f"Recall: {cv_results['test_recall'][i]}")
        print(f"F1-score: {cv_results['test_f1'][i]}\n")
    print("Average Metrics:")
    print(f"Average Accuracy: {np.mean(cv_results['test_accuracy'])}")
    print(f"Average Precision: {np.mean(cv_results['test_precision'])}")
    print(f"Average Recall: {np.mean(cv_results['test_recall'])}")
    print(f"Average F1 Score: {np.mean(cv_results['test_f1'])}\n")
    print("Lingspam Data Evaluation Metrics:")
    print(f"Accuracy: {lingspam_metrics['accuracy']}")
    print(f"Precision: {lingspam_metrics['precision']}")
    print(f"Recall: {lingspam_metrics['recall']}")
    print(f"F1 Score: {lingspam_metrics['f1']}")
