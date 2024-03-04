import hashlib
import json
from time import time 

# Representing a blockchain
class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # create the genesis block 
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):

        """
        Create the new block in the blockchain
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of the previous block 
        :return <dict> New Block 
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []
        self.chain.append(block)
        return block
    
    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transactions to go into the next mined block
        :param sender: <str> Address of the sender
        :param recipient: <str> Address of the recipient
        :param amoutn: <int> Amount 
        :return: <int> The index of the Block that will hold this transactions
        """
        
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    @staticmethod 
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> block
        :return: <str>
        """
        # We must make sure that the dictionary is ordered, or we will have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @@property
    def last_block(self):
        # returns the last_block in the chain
        return self.chain[-1]

def main():

    ...



if __name__=="__main__":
    main()
