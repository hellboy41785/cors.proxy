from flask import Flask, request, render_template
from requests import get
from flask import make_response
from flask_cors import CORS

# Create a new Flask app
app = Flask(__name__)
CORS(app, allowed_origins='*')

@app.route('/')
def home():
    return render_template('index.html')

@app.get('/proxy')
def proxy():
    url = request.args['url']
    print(url)
    
    url = get(url, headers = {
        "User-Agent": request.headers['User-Agent']
    })
    resp = make_response(url.text)
    resp.headers['Content-Type'] = url.headers['Content-Type']
    return resp

@app.post('/proxy')
def proxy_url_with_args():
    url = request.get_json()['url']
    print(url)
    if 'https://' not in url or 'http://' in url:
        return {"error": True, "message":"this proxy only allows proxying HTTPS requests"}
        
    url = get(url, headers = {
        "User-Agent": request.headers['User-Agent']
    })
    resp = make_response(url.text)
    resp.headers['Content-Type'] = url.headers['Content-Type']
    resp.headers['Proxy'] = "true"
    return resp

app.run(host='0.0.0.0')