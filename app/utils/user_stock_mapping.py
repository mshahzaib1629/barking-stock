from itertools import islice
from google.cloud.firestore_v1.base_query import FieldFilter

def batched(iterable, batch_size):
    it = iter(iterable)
    while batch := list(islice(it, batch_size)):
        yield batch

def get_firebase_filtered_users(users_collection_ref, symbols):
    

    batch_size = 30
    results = []

    for batch in batched(symbols, batch_size):
        query = users_collection_ref.where(filter=FieldFilter("favoriteStocks", "array_contains_any", batch ))
        results.extend(query.stream())
        
    users_data = {}
    
    for doc in results:
        if doc.id not in users_data.keys():
            users_data[doc.id] = doc.to_dict()
            users_data[doc.id]['id'] = doc.id
        
    return users_data.values()


def get_user_announcements(users, announcements):
    for user in users:
        user['relevantAnnouncements'] = []

        for announcement in announcements:
            if announcement['SYMBOL'] in user['favoriteStocks']:
                user['relevantAnnouncements'].append(announcement)
    
    return users