import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings

import chromadb

client = chromadb.PersistentClient(path="db/")

# collection = client.create_collection(name="movie_plots")

# plot1 = "A group of bandits stage a brazen train hold-up, only to find a determined posse hot on their heels."
# plot2 = "A greedy tycoon decides, on a whim, to corner the world market in wheat. This doubles the price of bread, forcing the grain's producers into charity lines and further into poverty. The film..."
# plot3 = "Cartoon figures announce, via comic strip balloons, that they will move - and move they do, in a wildly exaggerated style."

# collection.add(
#     documents = [plot1, plot2, plot3],
#     metadatas = [{"movie": "The Great Train Robbery"},{"movie": "A Corner in Wheat"},{'movie':'Winsor McCay, the Famous Cartoonist of the N.Y. Herald and His Moving Comics'}],
#     ids = ["id1", "id2", "id3"]
# )

collection = client.get_collection(name="movie_plots")

results = collection.query(
    query_texts=["war"],
    n_results=1
)

print(results["metadatas"])
