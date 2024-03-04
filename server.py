from bc import Blockchain
from flask import Flask, jsonify, request
from uuid import uuid4


app = Flask(__name__)

node_identifier = str(uuid4()).replace("-", "")

blockchain = Blockchain()

@app.route("/mine", methods=["GET"])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block["proof"]
    proof = blockchain.proof_of_work(last_proof)

    blockchain.new_transaction(sender="0", recipient=node_identifier, amount=1)

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    res = {
        "message": "Added",
        "index": block["index"],
        "transactions": block["transactions"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"]
    }
    return jsonify(res), 200

@app.route("/transactions/new", methods=["POST"])
def new_transactions():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return "Missing values", 400
    # create a new one
    index = blockchain.new_transaction(values["sender"], values["recipient"], values["amount"])
    res = {
        "message": f"Transaction will be added to the block {index}",
    }
    return jsonify(res), 201

@app.route("/chain", methods=["GET"])
def full_chain():
    res = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain)
    }
    return jsonify(res), 200


if __name__ == "__main__":
    app.run(debug=True)