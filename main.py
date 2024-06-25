import pandas as pd
import logging
from data_cleaning import DataCleaning
from data_extraction import DataExtraction
from database_utils import DatabaseUtills
from uploadDataToS3 import uploadDataToS3


from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)


    data_extractor = DataExtraction()
    data_cleaner = DataCleaning()
    database_class = DatabaseUtills()


    raw_data_csv = 'output.csv'  
    table1 = data_extractor.get_data_from_santander('file1.pdf', raw_data_csv)
    table = pd.read_csv(raw_data_csv)
    cleaned_data = data_cleaner.clean_santander_data(table)
    print("Cleaned Data:")
    print(cleaned_data.head())

    raw1 = 'output1.csv'  
    table2 = data_extractor.get_data_from_santander('file2.pdf', raw1)
    table2 = pd.read_csv(raw1)
    cleaned_data1 = data_cleaner.clean_santander_data(table2)
    print("Cleaned Data:")
    print(cleaned_data1.head(40))

    contat_dataset = data_cleaner.concat_and_sort_df_bydate(cleaned_data, cleaned_data1)
    print(contat_dataset.head(100))
    contat_dataset.to_csv('output_file_merged.csv', index=False)


    def categorize_transaction(description):
        description = description.lower()
        
        if any(term in description for term in ['food', 'restaurant', 'cafe', 'burger', 'pizza', 'dining', 'eatery', 'bistro','starbucks', 'coffee', 'kfc']):
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

    contat_dataset['Category'] = contat_dataset['Description'].apply(categorize_transaction)
    print("Data with Category:")
    print(contat_dataset.head())


    vectorizer = TfidfVectorizer()
    X = contat_dataset['Description'].astype(str)
    y = contat_dataset['Category']
    X_transformed = vectorizer.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_transformed, y, test_size=0.2, random_state=42)
    model = LogisticRegression(class_weight='balanced')
    model.fit(X_train, y_train)


    y_pred = model.predict(X_test)
    print("Accuracy:", model.score(X_test, y_test))
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    contat_dataset['Predicted Category'] = model.predict(vectorizer.transform(contat_dataset['Description'].astype(str)))
    print("Final Data with Predictions:")
    print(contat_dataset.head(100))
    contat_dataset.to_csv('ml_test_file.csv')


    database_ready = data_cleaner.clean_santander_data_for_postgres(contat_dataset)
    print(database_ready.head(30))




    creds_local = database_class.read_db_creds('local_db_creds.yaml')
    local_engine = database_class.init_db_engine(creds_local)
    local_tables = database_class.list_db_tables(local_engine)


    grouped = database_ready.groupby('Category')
    dfs = {category: group for category, group in grouped}
    print(dfs['Food'].head())
    for d in dfs:
        print(d)

    database_class.upload_to_db(dfs['Food'], 'food', creds_local)
    database_class.upload_to_db(dfs['Bills'], 'bills', creds_local)
    database_class.upload_to_db(dfs['Groceries'], 'groceries', creds_local)
    database_class.upload_to_db(dfs['Health'], 'health', creds_local)
    database_class.upload_to_db(dfs['Other'], 'other', creds_local)
    database_class.upload_to_db(dfs['Shopping'], 'shopping', creds_local)
    database_class.upload_to_db(dfs['Transport'], 'transport', creds_local)

    


    