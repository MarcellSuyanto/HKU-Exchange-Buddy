from vectorDB.vdb import *

CREATE_DB = False
RELEVANCE_THRESHOLD = 1.00

def main():
    if CREATE_DB:
        create_vector_db()
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

    query = {
        'course_code' : "COMP3314",
        'course_description': "This course introduces algorithms, tools, practices, and applications of machine learning. Topics include core methods such as supervised learning (classification and regression), unsupervised learning (clustering, principal component analysis), Bayesian estimation, neural networks; common practices in data pre-processing, hyper-parameter tuning, and model evaluation; tools/libraries/APIs such as scikit-learn, Theano/Keras, and multi/many-core CPU/GPU programming.",
        'home_university': 'HKU'
    }

    results_course_codes, results_course_desc, result_similarity = query_db(query, 5)
    course_counts = 0
    for i in range(len(results_course_codes)):
        if result_similarity[i] < RELEVANCE_THRESHOLD:
            print(results_course_codes[i])
            print(results_course_desc[i])
            print(f"Similarity rating: {(result_similarity[i]):.2f}")
            course_counts += 1
    if not course_counts:
        print("No relevant courses found")
        


if __name__ == "__main__":
    main()