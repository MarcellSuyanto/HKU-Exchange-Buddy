import chromadb

def create_hku_vector_db():
    client = chromadb.PersistentClient(path="HKUvectorDB")
    hku_collection = client.get_or_create_collection(name="hku_courses")


    return hku_collection 