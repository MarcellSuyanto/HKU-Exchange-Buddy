from vectorDB.HKUvdb import *

CREATE_DB = False

def main():
    if CREATE_DB:
        create_vector_db()

    query = {
        'course_code' : "CIVL20152",
        'course_description': "Materials 2 (Civil): The unit builds on and expands the topics of concrete, metals and corrosion which were introduced in Materials 1 (Civil). Additionally, polymer and glass materials are introduced.  In this unit the properties of these materials are illustrated with examples from construction practice.  Deterioration mechanisms (and their prevention) are examined in more detail.",
    }

    results_course_codes, results_course_desc, result_similarity = query_db(query, 3)
    for i in range(len(results_course_codes)):
        print(results_course_codes[i])
        print(results_course_desc[i])
        print(f"Similarity rating: {(1-result_similarity[i])*100:.2f}")


if __name__ == "__main__":
    main()