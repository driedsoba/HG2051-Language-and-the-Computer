import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data from 'SMSSpamCollection.txt into a DataFrame
data = pd.read_csv('datasets/SMSSpamCollection.txt', sep='\t', header=None, names=['label', 'message'])

# Define custom colours for count plot - blue for 'ham' and red for 'spam'
cols= ["#4878CF", "#D1495B"] 

# Set up the figure and axis for the count plot
plt.figure(figsize=(12,8))
fg = sns.countplot(data, x="label", palette=cols)

# Set title and labels for the count plot
fg.set_title("Distribution of Ham and Spam Messages")
fg.set_xlabel("Message Type")
fg.set_ylabel("Number of Messages")

# Display counts on top of each bar
for i in fg.containers:
    fg.bar_label(i)

# Save the plot as an image file
plt.savefig('countplot.png')


