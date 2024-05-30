import pandas as pd
import logging
from data_cleaning import DataCleaning
from data_extraction import DataExtraction
from uploadDataToS3 import uploadDataToS3

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    aws_access_key_id = 'AKIA435ULAGV54PPKQAC'
    aws_secret_access_key = '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'
    region_name = 'eu-west-1'


    data_extractor = DataExtraction()
    data_cleaner = DataCleaning()


    raw_data_csv = 'output.csv'  
    table1 = data_extractor.get_data_from_santander('file1.pdf', raw_data_csv)
    table = pd.read_csv(raw_data_csv)
    cleaned_data = data_cleaner.clean_santander_data(table)
    print("Cleaned Data:")
    print(cleaned_data.head())
    cleaned_data['Transaction Type'] = cleaned_data.apply(lambda row: 'Money in' if row['Money in'] > 0 else 'Money out', axis=1)
    print("Data with Transaction Type:")
    print(cleaned_data.head())
    X = cleaned_data['Description']
    y = cleaned_data['Transaction Type']
    vectorizer = TfidfVectorizer()
    X_transformed = vectorizer.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_transformed, y, test_size=0.2, random_state=42)
    model = LogisticRegression(class_weight='balanced')
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    print(f'Accuracy: {accuracy}')
    print('Classification Report:')
    print(report)

    cleaned_data['Predicted Transaction Type'] = model.predict(vectorizer.transform(cleaned_data['Description'].astype(str)))
    print("Final Data with Predictions:")
    print(cleaned_data.head())

    def categorize_transaction(description):
        description = description.lower()
        
        if any(term in description for term in ['food', 'restaurant', 'cafe', 'burger', 'pizza', 'dining', 'eatery', 'bistro']):
            return 'Food'
        elif any(term in description for term in ['bill', 'utilities', 'rent', 'subscription', 'membership', 'fee']):
            return 'Bills'
        elif any(term in description for term in ['tfl', 'travel', 'bus', 'train', 'flight', 'uber', 'taxi', 'transport']):
            return 'Transport'
        elif any(term in description for term in ['tesco', 'supermarket', 'groceries', 'market', 'store', 'shop', 'local']):
            return 'Groceries'
        elif any(term in description for term in ['netflix', 'cinema', 'movie', 'concert', 'theater', 'show', 'entertainment']):
            return 'Entertainment'
        elif any(term in description for term in ['amazon', 'shopping', 'clothing', 'apparel', 'boutique', 'mall', 'retail']):
            return 'Shopping'
        elif any(term in description for term in ['pharmacy', 'doctor', 'hospital', 'clinic', 'medical', 'health', 'dentist']):
            return 'Health'
        elif any(term in description for term in ['electricity', 'water', 'gas', 'internet', 'phone', 'utility']):
            return 'Utilities'
        else:
            return 'Other'

    cleaned_data['Category'] = cleaned_data['Description'].apply(categorize_transaction)
    print("Data with Category:")
    print(cleaned_data.head())

    cleaned_data['Money in'] = pd.to_numeric(cleaned_data['Money in'], errors='coerce').fillna(0)
    cleaned_data['Money out'] = pd.to_numeric(cleaned_data['Money out'], errors='coerce').fillna(0)

    cleaned_data['Transaction Type'] = cleaned_data.apply(lambda row: 'Money In' if row['Money in'] > 0 else 'Money Out', axis=1)
    print("Data with Transaction Type:")
    print(cleaned_data.head())

    vectorizer = TfidfVectorizer()
    X = cleaned_data['Description'].astype(str)
    y = cleaned_data['Category']
    X_transformed = vectorizer.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_transformed, y, test_size=0.2, random_state=42)
    model = LogisticRegression(class_weight='balanced')
    model.fit(X_train, y_train)

    # Make predictions and evaluate
    y_pred = model.predict(X_test)
    print("Accuracy:", model.score(X_test, y_test))
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    # Print the first few rows of the final DataFrame with predictions
    cleaned_data['Predicted Category'] = model.predict(vectorizer.transform(cleaned_data['Description'].astype(str)))
    print("Final Data with Predictions:")
    print(cleaned_data.head(100))
    cleaned_data.to_csv('ml_test_file.csv')
  

    
