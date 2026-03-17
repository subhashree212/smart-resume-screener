from app import create_app
from flask import send_file

app = create_app()

@app.route('/')
def index():
    return send_file('templates/index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
