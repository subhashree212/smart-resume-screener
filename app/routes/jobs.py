from flask import Blueprint, request, jsonify
from app.models.db import get_connection

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/jobs', methods=['POST'])
def create_job():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    if not title or not description:
        return jsonify({'error': 'title and description required'}), 400
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO jobs (title, description) VALUES (%s, %s)', (title, description))
    conn.commit()
    job_id = cursor.lastrowid
    conn.close()
    return jsonify({'message': 'Job created', 'job_id': job_id}), 201

@jobs_bp.route('/jobs', methods=['GET'])
def get_jobs():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM jobs ORDER BY created_at DESC')
    jobs = cursor.fetchall()
    conn.close()
    return jsonify({'jobs': jobs})

@jobs_bp.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM jobs WHERE id = %s', (job_id,))
    job = cursor.fetchone()
    conn.close()
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    return jsonify({'job': job})

@jobs_bp.route('/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM results WHERE job_id = %s', (job_id,))
    cursor.execute('DELETE FROM resumes WHERE job_id = %s', (job_id,))
    cursor.execute('DELETE FROM jobs WHERE id = %s', (job_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Job deleted'})
