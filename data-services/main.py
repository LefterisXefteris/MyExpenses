import pandas as pd
import logging
from data_cleaning import DataCleaning
from data_extraction import DataExtraction
from database_utils import DatabaseUtills
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import os

def categorize_transaction(description):
    description = description.lower()
    
    if any(term in description for term in ['food', 'restaurant', 'cafe', 'burger', 'pizza', 'dining', 'eatery', 'bistro','starbucks', 'coffee', 'kfc', 'CHICKEN']):
        return 'Food'
    elif any(term in description for term in ['bill', 'utilities', 'rent', 'subscription', 'membership', 'fee']):
        return 'Bills'
    elif any(term in description for term in ['tfl', 'travel', 'bus', 'train', 'flight', 'uber', 'taxi', 'transport']):
        return 'Transport'
    elif any(term in description for term in ['tesco', 'supermarket', 'groceries', 'market', 'store', 'shop', 'local', 'market']):
        return 'Groceries'
    elif any(term in description for term in ['netflix', 'cinema', 'movie', 'concert', 'theater', 'show', 'entertainment']):
        return 'Entertainment'
    elif any(term in description for term in ['amazon', 'shopping', 'clothing', 'apparel', 'boutique', 'mall', 'retail']):
        return 'Shopping'
    elif any(term in description for term in ['pharmacy', 'doctor', 'hospital', 'clinic', 'medical', 'health', 'dentist']):
        return 'Health'
    elif any(term in description for term in ['electricity', 'water', 'gas', 'internet', 'phone', 'utility']):
        return 'Utilities'
    elif any(term in description for term in ['lefteris']):
        return 'Not affect in funds'
    elif any(term in description for term in ['transfer']):
        return 'Money Transfer'
    else:
        return 'Other'

def preprocess_data(file1, file2, data_extractor, data_cleaner):
    # Extract and clean data from file1
    raw_data_csv = 'output.csv'
    if not os.path.exists(raw_data_csv):
        logging.info(f"{raw_data_csv} does not exist. Creating it now.")
        data_extractor.get_data_from_santander(file1, raw_data_csv)
    
    table = pd.read_csv(raw_data_csv)
    cleaned_data = data_cleaner.clean_santander_data(table)

    # Extract and clean data from file2
    raw1 = 'output1.csv'  
    data_extractor.get_data_from_santander(file2, raw1)
    table2 = pd.read_csv(raw1)
    cleaned_data1 = data_cleaner.clean_santander_data(table2)

    # Concatenate and sort datasets
    concat_dataset = data_cleaner.concat_and_sort_df_bydate(cleaned_data, cleaned_data1)
    
    # Categorize transactions
    concat_dataset['Category'] = concat_dataset['Description'].apply(categorize_transaction)
    
    return concat_dataset

def train_model(data):
    vectorizer = TfidfVectorizer()
    X = data['Description'].astype(str)
    y = data['Category']
    X_transformed = vectorizer.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_transformed, y, test_size=0.2, random_state=42)
    
    model = LogisticRegression(class_weight='balanced')
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    print("Accuracy:", model.score(X_test, y_test))
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    return model, vectorizer

def predict_categories(data, model, vectorizer):
    data['Predicted Category'] = model.predict(vectorizer.transform(data['Description'].astype(str)))
    return data

def main():
    logging.basicConfig(level=logging.INFO)

    data_extractor = DataExtraction()
    data_cleaner = DataCleaning()
    database_class = DatabaseUtills()

    # Preprocess data
    processed_data = preprocess_data('file1.pdf', 'file2.pdf', data_extractor, data_cleaner)
    processed_data.to_csv('output_file_merged.csv', index=False)

    # Train model and make predictions
    model, vectorizer = train_model(processed_data)
    final_data = predict_categories(processed_data, model, vectorizer)
    
    print("Final Data with Predictions:")
    print(final_data.head(100))
    final_data.to_csv('ml_test_file.csv')

    # Prepare data for database
    database_ready = data_cleaner.clean_santander_data_for_postgres(final_data)
    print(database_ready.head(50))

    # Database operations
    local_engine = database_class.init_db_engine()
    local_tables = database_class.list_db_tables(local_engine)

    data_for_categories_table = database_ready['Category'].unique()
    categories_df = pd.DataFrame(data_for_categories_table, columns=['categoryname'])
    print(categories_df.head(30))

    database_class.upload_to_db(categories_df, 'categories')

if __name__ == '__main__':
    main()