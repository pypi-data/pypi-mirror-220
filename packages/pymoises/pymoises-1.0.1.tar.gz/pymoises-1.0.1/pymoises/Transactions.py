import requests
import logging

from .dto import (
    create_transaction_input_schema,
    transaction_output_schema
)

class Transaction:
    def create_transaction(request: create_transaction_input_schema) -> transaction_output_schema:
        """
        Create transaction in moises.

        Params:
            create_transaction_input_schema : 
                idPsp (string): id from psp
                crmId (string): lead's phone
                amount (Int) 

        Return:
            transaction_output_schema:
                success (boolean): success function
                message (string): result of function
        """

        url = "http://crm-app.tech/api/crm/create-transaction"

        payload = {}
        payload['idPsp'] = request['idPsp']
        payload['crmId'] = request['crmId']
        payload['amount'] = request['amount']

        headers = {}
        headers['Content-Type'] = 'application/json'

        try:

            moisesResponse = requests.request("POST", url, headers=headers, json=payload)
            logging.warning('CREATE TRANSACTION IN MOISES %s' % (moisesResponse.text))
            moisesResponse = moisesResponse.json()

            if not moisesResponse['result'] == 1:
                respone : transaction_output_schema = {}
                respone['success'] = False
                respone['message'] = "Transaction not create"

                return respone

            respone : transaction_output_schema = {}
            respone['success'] = True
            respone['message'] = "Transaction create"
            respone['payload'] = {}
            return respone
    
        except Exception as Err:
            respone : transaction_output_schema = {}
            respone['success'] = False
            respone['message'] = str(Err)
            respone['payload'] = {}

            return respone