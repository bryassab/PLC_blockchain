import datetime
import hashlib
import json
import requests
from urllib.parse import urlparse


class Blockchain:

    def __init__(self):
        self.chains = []
        self.transactions = []
        self.create_block(name='', age='', email='', description='', proof=1,
                          previous_hash='0', genesis=True)
        self.nodes = set()

    def create_block(self, name, age, email, description, proof, previous_hash, genesis):
        if (genesis):
            block = {'index': len(self.chains) + 1,
                     'timestamp': str(datetime.datetime.now()),
                     'proof': proof,
                     'previous_hash': previous_hash,
                     'transactions': self.transactions}
        else:
            block = {'index': len(self.chains) + 1,
                     'name': name,
                     'age': age,
                     'email': email,
                     'description':description,
                     'timestamp': str(datetime.datetime.now()),
                     'proof': proof,
                     'previous_hash': previous_hash,
                     'transactions': self.transactions}
        self.chains.append(block)
        return block

    def get_previous_block(self):
        return self.chains[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(
                str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

    def add_transaction(self, index, sender, receiver, amount):
        for chain in self.chains:
            if chain['index'] == int(index):
                chain['transactions'].append({
                    'id': len(chain['transactions']) + 1,
                    'sender': sender,
                    'receiver': receiver,
                    'amount': amount,
                    'date': str(datetime.datetime.now())})
                return len(chain['transactions'])

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chains)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chains = longest_chain
            return True
        return False
