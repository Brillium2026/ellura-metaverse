from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    try:
        with open('static/index.html', 'r') as f:
            return f.read(), 200, {'Content-Type': 'text/html'}
    except:
        return """
        <html><body style='background:black;color:white;font-family:monospace;'>
        <h1>ELLURA DEPLOYMENT ERROR</h1>
        <p>Static file not found. Check GitHub repo structure.</p>
        <p>Status: Online</p>
        </body></html>
        """, 200, {'Content-Type': 'text/html'}
