import os
import sys
import pathlib
from flask_cors import CORS
# Crear el path del archivo actual
path = sys.path[0]
# Inserta en el sistema el folder principal como modulo
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent.parent))

# CREANDO UN BLOCKCHAIN
from datetime import datetime
from uuid import uuid4
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
from PLC_blockchain.app.models.blockchain import Blockchain

# Importar Blockchain Class

blockchain = Blockchain()

# Creando Web App
app = Flask(__name__,static_url_path='/public',static_folder='../public/uploads')
CORS(app)

# Creando Blockchain
blockchain = Blockchain()

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'rar', 'zip'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads', methods=['GET'])
def uploads():
    args = request.args
    month = args.get("month")
    data = {"pdf_files":[]}
    pdf_folder = str(pathlib.Path("app/public/uploads/pdf").resolve())
    compressed_folder = str(pathlib.Path("app/public/uploads/compressed").resolve())
    for pdf in os.listdir(pdf_folder):
        pdf_date = pdf.split(".")[0]
        pdf_extension = pdf.split(".")[1]
        json_pdf = {}
        if pdf_extension == "pdf":
            if month != None:
                number_month = pdf.split("-")[1]
                if month == number_month:
                    json_pdf["file_name"] = pdf;
                    json_pdf["path"] = "/public/pdf/" + pdf 
            else: 
                json_pdf["file_name"] = pdf;
                json_pdf["path"] = "/public/pdf/" + pdf
            
            for compressed in os.listdir(compressed_folder):
                compressed_extension = compressed.split(".")[1]
                compressed_date = compressed.split(".")[0]
                if compressed_extension == "rar" or compressed_extension == "zip":
                    if month != None:
                        number_month = compressed.split("-")[1]
                        if month == number_month:
                            if compressed_date == pdf_date:
                                json_pdf["compressed_file_name"] = compressed
                    else: 
                        if compressed_date == pdf_date:
                            json_pdf["compressed_file_name"] = compressed
                    
            if len(json_pdf) != 0:  
                data["pdf_files"].append(json_pdf)

    return jsonify(data), 200



# Minando un Nuevo Bloque
@app.route('/mine_block', methods=['POST'])
def mine_block():
    name = request.form['name']
    age = request.form['age']
    email = request.form['email']
    description = request.form['description']
    path_pdf = ''
    path_compressed = ''
    pdf_file = request.files['pdf']
    rar_zip = request.files['compressed']
    if pdf_file.filename == '' or rar_zip.filename == '':
        return jsonify({"message": "Por favor seleccione un archivo"}), 400
    if pdf_file and allowed_file(pdf_file.filename) and rar_zip and allowed_file(rar_zip.filename):
        # dd/mm/YY
        now = datetime.now()
        now_date = now.strftime("%d-%m-%Y %H:%M:%S")
        for lap in range(1,3):
            file = pdf_file
            if lap == 2: file = rar_zip
            file_extension = pathlib.Path(file.filename).suffix
            filename = secure_filename(now_date + file_extension)
            folder = "compressed"
            if file_extension.split(".")[1] == "rar" or file_extension.split(".")[1] == "zip": 
                path_compressed = f'/public/{folder}/{filename}'
            if file_extension.split(".")[1] == "pdf": 
                folder = "pdf"
                path_pdf = f'/public/{folder}/{filename}'
            file.save(os.path.join(f'app/public/uploads/{folder}', filename))
    else:
        return jsonify({"message": "Extensiones no soportadas"}), 400
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(
        name, age, email, description, path_pdf, path_compressed, proof, previous_hash, genesis=False)
    return jsonify(block), 200


# Obteniendo todas las cadenas
@app.route('/get_chains', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chains,
                'length': len(blockchain.chains)}
    return jsonify(response), 200

# Obteniendo una cadena
@app.route('/get_chains/<index>', methods=['GET'])
def get_one_chain(index):
    for chain in blockchain.chains:
        if chain['index'] == int(index):
            return jsonify(chain), 200
    return jsonify({'message': 'Content not found'}), 404

# Chequeando validez de cadena de bloques


@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chains)
    if is_valid:
        response = {'message': 'Todo bien. El BLockchain es valido'}
    else:
        response = {
            'message': 'Houston, tenemos un problema. El blockchain no es valido!'}
    return jsonify(response), 200

# Agregando nueva transaccion al blockchain


@app.route('/add_transaction/<index>', methods=['PATCH'])
def add_transaction(index):
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all(key in json for key in transaction_keys):
        return 'Algun elemento de la transaccion esta faltando', 400

    id = blockchain.add_transaction(
        index, json['sender'], json['receiver'], json['amount'])
    response = {
        'message': f'La transaccion sera añadida con el id N°{id} al bloque.'}
    return jsonify(response), 201

# Paso 3 - Descentralizando el Blockchain

# Conectando Nuevos Nodos
@app.route('/connect_node', methods=['POST']) #Unused
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No node", 401
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'Todos los nodos estan ahora conectados. El plcCoin Blockchain contiene los siguientes nodos:',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201

# Remplazando la Cadena por la Mas Larga
@app.route('/replace_chain', methods=['POST'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'Los nodos tenian diferentes cadenas asi que la cadena fue remplazada por la mas larga',
                    'new_chain': blockchain.chains}
    else:
        response = {'message': 'Todo bien. la cadena es la mas larga',
                    'actual_chain': blockchain.chains}
    return jsonify(response), 200


# Corriendo el App
app.run(host='0.0.0.0', port='5001')
