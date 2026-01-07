import chromadb
import pandas as pd
import os


def get_hku_courses():
    departments = ["BUSI","ENGG"]
    courses = {
        "BUSI":[],
        "ENGG":["COMP","CIVL","BMED"]
    }
    df = pd.DataFrame()
    for department in departments:
        codes = courses[department]
        for code in codes:
            file_path = f"vectorDB/HKUCourseOutlines/{department}/{code}.csv"
            data = pd.read_csv(file_path)
            df = pd.concat([df, data], ignore_index=True)
    return df
            
def get_exchange_courses():
    
    pass

def create_vector_db():
    client = chromadb.PersistentClient(path="courseDB")
    collection = client.get_or_create_collection(name="courses")
    courses_df = get_hku_courses()

    course_codes = courses_df['course_code'].to_list()
    course_title_descriptions = courses_df["course_description"].to_list()
    metadata = []
    for i in range(len(courses_df)):
        temp = courses_df.iloc[i, 2:].to_dict()
        metadata.append(temp)
        
    collection.add(
        ids = course_codes,
        documents=course_title_descriptions,
        metadatas= metadata
    )
    client.clear_system_cache()
    return collection 

def query_db(query:dict, n_results=5):
    client = chromadb.PersistentClient(path="courseDB")
    collection = client.get_collection(name="courses")
    desc = query.get("course_description","")
    filters = {}
    if uni := query.get("University"):
        filters["University"] = uni
    if country := query.get("Country"):
        filters["Country"] = country

    if len(filters) > 1:
        where_clause = {"$and": [{k: v} for k, v in filters.items()]}
    else:
        where_clause = filters if filters else None

    results = collection.query(
        query_texts = [desc],
        n_results = n_results,
        where = where_clause
    )

    result_similarity = results['distances'][0]
    results_course_codes = results["ids"][0]
    results_course_desc = results["documents"][0]

    return results_course_codes, results_course_desc, result_similarity
