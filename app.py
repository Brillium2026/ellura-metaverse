@app.route('/')
def index():
    from flask import send_file
    return send_file('static/index.html')
