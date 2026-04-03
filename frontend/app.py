
import os
import logging
import requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Configuration par variables d'environnement
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:5001')
LOG_LEVEL   = os.environ.get('LOG_LEVEL', 'DEBUG')

# Configuration des logs (trop verbeux volontairement)
logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html><html><head><title>DevSecOps App</title>
<style>body{font-family:Arial;margin:40px;background:#f4f4f4;}
.card{background:white;padding:20px;border-radius:8px;margin:10px 0;box-shadow:0 2px 4px rgba(0,0,0,.1);}
button{background:#2E75B6;color:white;border:none;padding:10px 20px;border-radius:4px;cursor:pointer;}
pre{background:#f0f0f0;padding:10px;border-radius:4px;}</style></head>
<body><h1>Application DevSecOps — Phase 1</h1>
<div class=card><h2>Ajouter un utilisateur</h2>
<input id=uname placeholder='Nom utilisateur' style='padding:8px;margin:5px;'>
<input id=uemail placeholder='Email' style='padding:8px;margin:5px;'>
<button onclick=addUser()>Ajouter</button></div>
<div class=card><h2>Liste des utilisateurs</h2>
<button onclick=loadUsers()>Charger</button>
<pre id=result>Cliquez sur Charger...</pre></div>
<div class=card><h2>Health Check</h2>
<button onclick=healthCheck()>Vérifier</button>
<pre id=health></pre></div>
<script>
async function loadUsers(){
  const r=await fetch('/api/users');
  const d=await r.json();
  document.getElementById('result').textContent=JSON.stringify(d,null,2);}
async function addUser(){
  const n=document.getElementById('uname').value;
  const e=document.getElementById('uemail').value;
  const r=await fetch('/api/users',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:n,email:e})});
  const d=await r.json();
  document.getElementById('result').textContent=JSON.stringify(d,null,2);}
async function healthCheck(){
  const r=await fetch('/api/health');
  const d=await r.json();
  document.getElementById('health').textContent=JSON.stringify(d,null,2);}
</script></body></html>
'''

@app.route('/')
def index():
    logger.debug(f'Requete recue depuis IP: {request.remote_addr}')
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/users', methods=['GET'])
def get_users():
    logger.info(f'[APP1] GET /api/users -> forwarding to {BACKEND_URL}')
    try:
        resp = requests.get(f'{BACKEND_URL}/api/users')
        logger.debug(f'[APP1] Reponse backend: {resp.text}')
        return jsonify(resp.json())
    except Exception as e:
        logger.error(f'[APP1] Erreur backend: {e}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.get_json()
    logger.info(f'[APP1] POST /api/users data={data}')  # RISQUE: log donnees utilisateur
    try:
        resp = requests.post(f'{BACKEND_URL}/api/users', json=data)
        return jsonify(resp.json())
    except Exception as e:
        logger.error(f'[APP1] Erreur: {e}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health():
    try:
        resp = requests.get(f'{BACKEND_URL}/api/health')
        return jsonify({'frontend': 'ok', 'backend': resp.json()})
    except Exception as e:
        return jsonify({'frontend': 'ok', 'backend': 'unreachable', 'error': str(e)})

if __name__ == '__main__':
    logger.info(f'[APP1] Demarrage Frontend — BACKEND_URL={BACKEND_URL}')
    app.run(host='0.0.0.0', port=5000, debug=True)
