import pymongo
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import time

client = pymongo.MongoClient("mongodb+srv://shristy:eyMSwe1cYvubXYEG@cluster0.ofmz9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.sample_mflix
collection = db.movies

def get_sentence_embedding(sentence: str):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    sentence_embedding = model.encode(sentence)
    return sentence_embedding

query = "alien in town"


def get_all_movie_data():
    movie_data = []
    for document in collection.find({'plot_embedding':{"$exists":True}}):
        movie_data.append((document["_id"], document["plot_embedding"], document["title"], document["plot"]))
    return movie_data

def search_movies(query: str):
    query_embedding = get_sentence_embedding(query)
    movie_data = get_all_movie_data()
    all_plot_embeddings = [movie[1] for movie in movie_data]
    similarities = cosine_similarity([query_embedding], all_plot_embeddings)[0]
    movie_similarities = [(similarity, movie_id, title, plot) for similarity, (movie_id, _, title, plot) in zip(similarities, movie_data)]
    movie_similarities.sort(reverse=True, key=lambda x: x[0])
    top_movies = movie_similarities[:4]

    return top_movies

start_time = time.time()

results = search_movies(query)
for result in results:
    print(f'Movie Name: {result[2]}, \nMovie Plot: {result[3]}\n')


end_time = time.time()
time_taken = end_time - start_time
print(f"Time taken for the search: {time_taken:.4f} seconds")