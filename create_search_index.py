import pymongo
from sentence_transformers import SentenceTransformer

client = pymongo.MongoClient("mongodb+srv://shristy:eyMSwe1cYvubXYEG@cluster0.ofmz9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.sample_mflix
collection = db.movies


def get_sentence_embedding(sentence: str):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    sentence_embedding = model.encode(sentence)
    return sentence_embedding  

index_definition = {
    "mappings": {
        "fields": {
            "plot_embedding": {
                "type": "vector", 
                "subtype": "dense_float",  
                "dimension": 384
            }
        }
    }
}

response = collection.create_search_index(
    name="movie_plot_vector_index", 
    type="vector",
    definition=index_definition
)

query = "something war"

pipeline = [
    {
        "$search": {
            "index": "movie_plot_vector_index", 
            "knn": {
                "vector": get_sentence_embedding(query).tolist(), 
                "path": "plot_embedding", 
                "k": 3, 
                "num_threads": 4, 
                "metric": "cosine"  
            }
        }
    },
    {
        "$limit": 4
    }
]

results = collection.aggregate(pipeline)


for result in results:
    print(result)