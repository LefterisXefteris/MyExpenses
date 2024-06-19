class ModelClassification:
    def __init__(self):
        pass

    def categorize_transaction(self, description):
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
        else:
            return 'Other'
        
    