from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import time
import json
import os
from ..config import settings

pc = Pinecone(api_key=settings.PINECONE_API_KEY)

index_name = "restaurant-search"

index = None

def init_vector_index():
    print("Creating Pinecone index...")
    global index
    if not pc.has_index(index_name):
        pc.create_index(
            name=index_name,
            dimension=1024,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        print("Index created successfully!")
        while not pc.describe_index(index_name).status['ready']:
            time.sleep(1)
        index = pc.Index(index_name)
        print("Index is ready!")
        restaurants_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(restaurants_dir, "restaurants.json")
        with open(file_path) as f:
            restaurants = json.load(f)
        restaurant_texts = [restaurant["text_for_embedding"] for restaurant in restaurants]

        embeddings = pc.inference.embed(
            model="multilingual-e5-large",
            inputs=restaurant_texts,
            parameters={
                "input_type": "passage",
                "truncate": "END"
            }
        )
        records = []
        for restaurant, embedding in zip(restaurants, embeddings):
            records.append({
                "id": str(restaurant["id"]),
                "values": embedding["values"],
                "metadata": {
                    "name": restaurant["name"],
                    "cuisine": restaurant["cuisine"],
                    "area": restaurant["area"],
                    "price_range": restaurant["price_range"],
                    "ambiance": restaurant["ambiance"],
                    "description": restaurant["description"],
                    "specialties": restaurant["specialties"],
                    "dietary_options": restaurant["dietary_options"],
                    "features": restaurant["features"],
                    "phone": restaurant['contact']["phone"],
                    "address": restaurant['contact']["address"],
                    "email": restaurant['contact']["email"],
                    "website": restaurant['contact']["website"],
                    "hours": restaurant['contact']["hours"],
                    "reservation_required": restaurant['contact']["reservation_required"]
                }
            })
    
        index.upsert(
            vectors=records,
            namespace="restaurants"
        )
        print(f"Upserted {len(records)} restaurant records to Pinecone")
    else:
        index = pc.Index(index_name)
        print("Index already exists, skipping creation.")
        print("Index stats:", index.describe_index_stats())


def delete_index():
    global index
    print("Deleting Pinecone index...")
    if pc.has_index(index_name):
        pc.delete_index(index_name)
        index = None 
    print("Index deleted successfully!")

def get_pinecone_index():
    global index
    if index is None:
        if not pc.has_index(index_name):
            init_vector_index()
        else:
            index = pc.Index(index_name)
    return index

def search_restaurants(query,filter_dict=None,top_k=5):
    """
    This function searches for restaurants based on the user query in the vector database.
    """
    index = get_pinecone_index()
    query_embedding = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[query],
        parameters={"input_type": "query"}
    )
    results = index.query(
        namespace="restaurants",
        vector=query_embedding[0]["values"],
        filter=filter_dict,
        top_k=top_k,
        include_metadata=True
    )
    return results


def format_search_results_for_llm(results):
    """
    Helper function to format the search results from vector database to nice text to include in the context for the LLM
    """
    if not results or "matches" not in results or not results["matches"]:
        return "No restaurants found matching your criteria."
    formatted_context = "RESTAURANT SEARCH RESULTS:\n\n"
    for i, match in enumerate(results["matches"], 1):
        restaurant = match["metadata"]
        similarity_score = match["score"]
        formatted_context += f"RESTAURANT #{i} (Relevance Score: {similarity_score:.2f})\n"
        formatted_context += f"Name: {restaurant['name']}\n"
        formatted_context += f"Cuisine: {restaurant['cuisine']}\n"
        formatted_context += f"Location: {restaurant['area']}\n"
        formatted_context += f"Price Range: {restaurant['price_range']}\n"
        formatted_context += f"Ambiance: {restaurant['ambiance']}\n"
        formatted_context += f"Description: {restaurant['description']}\n"
        formatted_context += f"Specialties: {restaurant['specialties']}\n"
        formatted_context += f"Dietary Options: {restaurant['dietary_options']}\n"
        formatted_context += f"Contact:\n"
        formatted_context += f"\tPhone: {restaurant['phone']}\n"
        formatted_context += f"\tAddress: {restaurant['address']}\n"
        formatted_context += f"\tEmail: {restaurant['email']}\n"
        formatted_context += f"\tWebsite: {restaurant['website']}\n"
        formatted_context += f"\tHours: {restaurant['hours']}\n"
        formatted_context += f"\tReservation Required: {restaurant['reservation_required']}\n"
        formatted_context += f"Features: {restaurant['features']}\n\n"
    return formatted_context