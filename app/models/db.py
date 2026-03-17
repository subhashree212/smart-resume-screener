import pymysql
from config import Config

def get_connection():
    return pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

def init_db():
    conn = pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS resume_screener")
    cursor.execute("USE resume_screener")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            job_id INT NOT NULL,
            name VARCHAR(200),
            content TEXT NOT NULL,
            score FLOAT DEFAULT 0,
            status ENUM("queued","scored","failed") DEFAULT "queued",
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (job_id) REFERENCES jobs(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            job_id INT NOT NULL,
            resume_id INT NOT NULL,
            score FLOAT,
            reasoning TEXT,
            rank_pos INT,
            FOREIGN KEY (job_id) REFERENCES jobs(id),
            FOREIGN KEY (resume_id) REFERENCES resumes(id)
        )
    ''')
    conn.commit()
    conn.close()
    print("Database ready!")
