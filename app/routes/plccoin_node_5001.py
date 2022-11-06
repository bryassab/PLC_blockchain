import sys
import pathlib
# Crear el path del archivo actual
path = sys.path[0]
# Inserta en el sistema el folder principal como modulo
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent.parent))

# CREANDO UN BLOCKCHAIN
from uuid import uuid4
from flask import Flask, jsonify, request
from PLC_blockchain.app.models.blockchain import Blockchain

# Importar Blockchain Class

blockchain = Blockchain()

# Creando Web App
app = Flask(__name__)

# Minando un Nuevo Bloque


@app.route('/mine_block', methods=['POST'])
def mine_block():
    json = request.get_json()
    name = json['name']
    age = json['age']
    email = json['email']
    description = json['description']
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(
        name, age, email, description, proof, previous_hash, genesis=False)
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
@app.route('/connect_node', methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No node", 401
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'Todos los ndoos estan ahora conectados. El plcCoin Blockchain contiene los siguientes nodos:',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201

# Remplazando la Cadena por la Mas Larga
@app.route('/replace_chain', methods=['GET'])
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
