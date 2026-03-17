from flask import Blueprint, request, jsonify
from app.models.db import get_connection
from app.services.parser import parse_pdf, parse_text
from app.services.scorer import rank_resumes

resumes_bp = Blueprint('resumes', __name__)

@resumes_bp.route('/jobs/<int:job_id>/resumes', methods=['POST'])
def upload_resume(job_id):
    name = request.form.get('name', 'Unknown')
    if 'file' in request.files:
        file = request.files['file']
        content = parse_pdf(file.read())
    elif request.is_json:
        content = parse_text(request.get_json().get('content', ''))
    else:
        return jsonify({'error': 'No resume provided'}), 400
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO resumes (job_id, name, content, status) VALUES (%s, %s, %s, "queued")',
                   (job_id, name, content))
    conn.commit()
    resume_id = cursor.lastrowid
    conn.close()
    return jsonify({'message': 'Resume uploaded', 'resume_id': resume_id}), 201

@resumes_bp.route('/jobs/<int:job_id>/screen', methods=['POST'])
def screen_resumes(job_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM jobs WHERE id = %s', (job_id,))
    job = cursor.fetchone()
    if not job:
        conn.close()
        return jsonify({'error': 'Job not found'}), 404
    cursor.execute('SELECT * FROM resumes WHERE job_id = %s', (job_id,))
    resumes = cursor.fetchall()
    if not resumes:
        conn.close()
        return jsonify({'error': 'No resumes found for this job'}), 404
    ranked = rank_resumes(job['description'], resumes)
    for r in ranked:
        cursor.execute('''
            INSERT INTO results (job_id, resume_id, score, rank_pos)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE score=%s, rank_pos=%s
        ''', (job_id, r['resume_id'], r['score'], r['rank'], r['score'], r['rank']))
        cursor.execute('UPDATE resumes SET score=%s, status="scored" WHERE id=%s',
                       (r['score'], r['resume_id']))
    conn.commit()
    conn.close()
    return jsonify({'job_id': job_id, 'total_resumes': len(ranked), 'results': ranked})

@resumes_bp.route('/jobs/<int:job_id>/results', methods=['GET'])
def get_results(job_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT r.name, r.score, r.status, res.rank_pos, res.reasoning
        FROM resumes r
        JOIN results res ON r.id = res.resume_id
        WHERE r.job_id = %s
        ORDER BY res.rank_pos ASC
    ''', (job_id,))
    results = cursor.fetchall()
    conn.close()
    return jsonify({'job_id': job_id, 'results': results})

@resumes_bp.route('/jobs/<int:job_id>/resumes', methods=['GET'])
def get_resumes(job_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM resumes WHERE job_id = %s ORDER BY created_at DESC', (job_id,))
    resumes = cursor.fetchall()
    conn.close()
    return jsonify({'resumes': resumes})
