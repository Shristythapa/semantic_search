import pymongo
from sentence_transformers import SentenceTransformer

client = pymongo.MongoClient("mongodb+srv://shristy:eyMSwe1cYvubXYEG@cluster0.ofmz9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.sample_mflix
collection = db.movies

def get_sentence_embedding(sentence: str):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    sentence_embedding = model.encode(sentence)
    return sentence_embedding

query = "good"

results = collection.aggregate([
    { 
        "$vectorSearch": {
            "queryVector": get_sentence_embedding(query).tolist(),
            "path": "plot_embedding",
            "limit": 4,
            "numCandidates": 50,  
            "index": "PlotSemanticSearch"
        }
    }
])
# print(results)
# for document in results:
#     print(f'Movie Name: {document["title"]}, \nMovie Plot: {document["plot"]}\n')

# Convert cursor to a list and iterate
movies = list(results)  # Fetch all results into a list

if not movies:
    print("No movies found!")  # Handle empty results
else:
    for document in movies:
        print(f'Movie Name: {document["title"]}, \nMovie Plot: {document["plot"]}\n')