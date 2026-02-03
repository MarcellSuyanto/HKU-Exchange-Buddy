import chromadb
import pandas as pd
import os


def get_courses():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    root= os.path.join(base_dir, "CourseOutlines")
    df_list = []
    for root, dirs, files in os.walk(root):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                try:
                    data = pd.read_csv(file_path)
                    df_list.append(data)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    if df_list:
        df = pd.concat(df_list, ignore_index=True)
        return df
    else:
        print("No files found")
        return pd.DataFrame()
    
def create_vector_db():
    client = chromadb.PersistentClient(path="courseDB")
    collection = client.get_or_create_collection(name="courses")
    print("Retrieving University Courses...")
    courses_df = get_courses()
    print("Courses Retrieved!\n")

    course_codes = courses_df['course_code'].to_list()
    course_title_descriptions = courses_df["course_description"].to_list()
    metadata = []
    for i in range(len(courses_df)):
        temp = courses_df.iloc[i, 2:].to_dict()
        metadata.append(temp)
    
    print("Creating Vector Database...")
    collection.add(
        ids = course_codes,
        documents=course_title_descriptions,
        metadatas= metadata
    )
    client.clear_system_cache()
    print("Vector Database Created!\n")
    return collection 

def get_credit_database(course_code, faculty, home_uni):
    #Extended feature, do when have time
    file_paths = {
        "Engineering": "./creditData/engg-credit-transfer",
        "Business": "./creditData/business-credit-transfer"
    }

    
    if home_uni and course_code:
        if home_uni == "HKU" and faculty:
            # Search specific faculty database
            pass
        elif home_uni == "HKU" and not faculty:
            # Iterate through all databases
            pass


def query_db(query:dict, n_results=5):
    print("Processing query...")
    """
    query->
    {
    course_code: The course code of the queried course
    course_description: The course description of the queried course
    course_faculty: HKU only, faculty of the course
    home_university: The original university
    host_university: The university being visited
    host_country: The country being visited
    }
    """

    client = chromadb.PersistentClient(path="courseDB")
    collection = client.get_collection(name="courses")
    code = query.get("course_code","")
    desc = query.get("course_description","")
    faculty = query.get("course_faculty")

    filters = {}
    if home_uni := query.get("home_university"):
        filters["home_university"] = home_uni
    if host_uni := query.get("host_university"):
        filters["host_university"] = host_uni   
    if host_country := query.get("host_country"):
        filters["host_country"] = host_country

    """
    LOGIC FLOW
    - If home_university AND course_code OR faculty OR host_university OR host_country EXISTS:
        Check credit transfer database accordingly

    - If host_university AND NOT host_country EXISTS:
        Filter only by university name

    - If NOT host_university AND host_country EXISTS:
        Filter only by country, exclude home_university

    - If host_university AND host_country EXISTS:
        Filter only by university name 
        
    - If NOT host_university AND NOT home_country EXISTS:
        Only filter by excluding home_university
    """
    credit_db = []
    where_clause = dict()
    
    if host_uni:
        where_clause["University"] = host_uni
    else:
        if host_country:
            where_clause["$and"] = [{'University': {"$ne": home_uni}}, {'Country': host_country}]
        else:
            where_clause["University"] = {"$ne":home_uni}

    results = collection.query(
        query_texts = [desc],
        n_results = n_results,
        where = where_clause if where_clause else None
    )

    result_similarity = results['distances'][0]
    results_course_codes = results["ids"][0]
    results_course_desc = results["documents"][0]

    return results_course_codes, results_course_desc, result_similarity
