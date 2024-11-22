import requests
import os
from dotenv import load_dotenv
from utils import retry_on_error
from auth import generate_jwt

load_dotenv()

TRANSACTIONS_SERVICE_URL = os.getenv('TRANSACTIONS_SERVICE_URL')
USERS_SERVICE_URL = os.getenv('USERS_SERVICE_URL')

def process_refund(message):
    try:
        transaction_id = message['transaction_id']
        sender_id = message['sender_id']
        amount = message['amount']

        def check_transaction_status():
            print(f"{TRANSACTIONS_SERVICE_URL}/transaction/{transaction_id}")
            response = requests.get(f"{TRANSACTIONS_SERVICE_URL}/transaction/{transaction_id}")
            return response

        transaction_status = retry_on_error(check_transaction_status)

        if not transaction_status:
            print(f"Error: Unable to fetch transaction {transaction_id}")
            return

        transaction = transaction_status.json().get('data', {})
        if transaction.get('status') != 'FAILED':
            print(f"Transaction {transaction_id} is not in FAILED state.")
            return

        refund_payload = {
            "user_id": sender_id,
            "transaction_type": "CREDIT",
            "amount": amount
        }

        token = generate_jwt(sender_id)

        def initiate_refund():
            return requests.post(f"{USERS_SERVICE_URL}/users/transaction",json=refund_payload,headers={"Authorization": f"Bearer {token}"},)

        response = retry_on_error(initiate_refund)

        if response and response.status_code == 200:
            print(f"Refund processed for transaction {transaction_id}")
        else:
            print(f"Failed to process refund for transaction {transaction_id}: {response.text}")

    except Exception as e:
        print(f"Error processing refund: {e}")
