from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def score_resume(job_description, resume_text):
    corpus = [job_description, resume_text]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(corpus)
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    score_percent = round(float(score) * 100, 2)

    keywords = vectorizer.get_feature_names_out()
    job_vec = tfidf_matrix[0].toarray()[0]
    resume_vec = tfidf_matrix[1].toarray()[0]

    matched = []
    missing = []
    for i, word in enumerate(keywords):
        if job_vec[i] > 0:
            if resume_vec[i] > 0:
                matched.append(word)
            else:
                missing.append(word)

    return {
        'score': score_percent,
        'matched_keywords': matched[:10],
        'missing_keywords': missing[:10]
    }

def rank_resumes(job_description, resumes):
    results = []
    for resume in resumes:
        result = score_resume(job_description, resume['content'])
        results.append({
            'resume_id': resume['id'],
            'name': resume['name'],
            'score': result['score'],
            'matched_keywords': result['matched_keywords'],
            'missing_keywords': result['missing_keywords']
        })
    results.sort(key=lambda x: x['score'], reverse=True)
    for i, r in enumerate(results):
        r['rank'] = i + 1
    return results
