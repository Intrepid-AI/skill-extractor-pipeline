import numpy as np

from gensim.models import Word2Vec

from sklearn.metrics.pairwise import cosine_similarity

def resume_jd_skills_matching(unique_skills_resume,unique_skills_jd):
    # Train Word2Vec model on a corpus of skills
    corpus = [unique_skills_jd,unique_skills_resume] # Combine both lists into a corpus
    model = Word2Vec(corpus, min_count=1,)  # Train the Word2Vec model
    # Calculate average vector representations for each list of skills
    vector1 = np.mean([model.wv[skill] for skill in unique_skills_jd if skill in model.wv], axis=0)
    vector2 = np.mean([model.wv[skill] for skill in unique_skills_resume if skill in model.wv], axis=0)

    # Reshape the vectors if necessary
    vector1 = vector1.reshape(1, -1)  # Reshape to a row vector
    vector2 = vector2.reshape(1, -1)  # Reshape to a row vector

    # Calculate cosine similarity
    similarity_matrix = cosine_similarity(vector1, vector2)
    match_percentage = similarity_matrix[0][0]*100
    return match_percentage