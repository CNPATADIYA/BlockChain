from flask import Flask, jsonify, request
from blockchain import Blockchain

bchain = Blockchain()


app = Flask(__name__)

@app.route("/")
def welcome():
    return "<p>Welcome to Hacker's blockchain</p>"

@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
        'chain': bchain.chain,
        'length': len(bchain.chain)
    }
    return jsonify(response), 200

@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_v = bchain.is_chain_valid(bchain.chain)

    if is_v:
        response = {'message': 'All good. The ledger is valid'}
    else:
        response = {'message': 'Opps. Not Valid'}
    
    return jsonify(response), 200

@app.route('/mine_block', methods=['POST'])
def mine_block():
    values = request.get_json()

    required = ['owner', 'Reg_no']

    if not all(x in values for x in required):
        return 'Missing Values', 400
    
    owner = values['owner']
    Reg_no = values['Reg_no']
    previous_block = bchain.get_last_block()
    previous_proof = previous_block['proof']
    proof = bchain.proof_of_work(previous_proof)
    previous_hash = bchain.hash(previous_block)
    block = bchain.create_block(owner, Reg_no, proof, previous_hash)

    response = {'message' : 'Record added to Blockchain'}

    return jsonify(response), 200

app.run(port=8080, debug=True)