import pymongo
from sentence_transformers import SentenceTransformer

client = pymongo.MongoClient("mongodb+srv://shristy:eyMSwe1cYvubXYEG@cluster0.ofmz9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.sample_mflix
collection = db.movies

def get_sentence_embedding(sentence: str):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    sentence_embedding = model.encode(sentence)
    return sentence_embedding   

for doc in collection.find({'plot':{"$exists":True}}).limit(50):
    print(f"embedding: {get_sentence_embedding(doc['plot'])}")
    doc['plot_embedding'] = get_sentence_embedding(doc['plot']).tolist()
    print("created and added embedding")
    collection.replace_one({'_id':doc['_id']},doc)

# Get the total number of documents in the collection
# count = collection.count_documents({})
# print(f"Number of documents in the collection: {count}")
