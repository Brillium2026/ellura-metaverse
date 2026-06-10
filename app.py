from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def index():
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'static', 'index.html')
        with open(file_path, 'r') as f:
            return f.read(), 200, {'Content-Type': 'text/html'}
    except Exception:
        return "<html><body style='background:black;color:white;'><h1>ELLURA</h1><p>Status: Online</p></body></html>", 200, {'Content-Type': 'text/html'}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
