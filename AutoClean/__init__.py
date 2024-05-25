import pandas as pd
from autoclean import AutoClean

# Load the Titanic dataset
titanic_data = pd.read_csv('Titanic-Dataset.csv')

# Instantiate the AutoClean class with default parameters
cleaner = AutoClean(titanic_data)

# Access the cleaned DataFrame
cleaned_data = cleaner.output

# Print the first few rows of the cleaned DataFrame
print(cleaned_data.head())
