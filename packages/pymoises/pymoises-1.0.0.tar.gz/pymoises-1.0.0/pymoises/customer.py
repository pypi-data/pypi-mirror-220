import requests
import logging

from .dto import (
    check_email_phone_input_schema,
    get_customer_output_schema
)

class Customers:
    def check_customer_by_email_phone(request: check_email_phone_input_schema) -> get_customer_output_schema:
        """
        Check if exist a customer in moises whit the email and phone.

        Params:
            check_email_phone_input_schema : 
                email (string): lead's email
                phone (string): lead's phone

        Return:
            get_customer_output_schema:
                success (boolean): success function
                message (string): result of function
                payload (dict) -- OPTIONAL:
                    tpid (string): if customer exist return tpid
        """
        url = "http://webservicesnt.org:5050/check-if-exist-customer"

        payload = {}
        payload['email'] = request['email']
        payload['phone'] = request['phone']

        headers = {}
        headers['Content-Type'] = 'application/json'

        try:

            moisesResponse = requests.request("POST", url, headers=headers, json=payload)
            logging.warning('RESPONE CHECK IF EXIST IN MOISES %s' % (moisesResponse.text))
            moisesResponse = moisesResponse.json()

            if not moisesResponse['result'] == 1:
                respone : get_customer_output_schema = {}
                respone['success'] = False
                respone['message'] = "Customer exist"
                respone['payload'] = {}
                respone['payload']['tpid'] = moisesResponse['data'][0]['tpId']

                return respone

            respone : get_customer_output_schema = {}
            respone['success'] = True
            respone['message'] = "Customer not exist"
            respone['payload'] = {}
            return respone
    
        except Exception as Err:
            respone : get_customer_output_schema = {}
            respone['success'] = False
            respone['message'] = str(Err)
            respone['payload'] = {}

            return respone
        
    def get_info_by_tpid(tpid: str):
        """
        Get info of customer by tpid.

        Params:
            tpid (string) :  lead's tpid

        Return:
            get_customer_output_schema:
                success (boolean): success function
                message (string): result of function
                payload (dict) -- OPTIONAL:
                    tpid (string): if customer exist return tpid
        """
        url = "http://webservicesnt.org:5050/customer/info"

        payload = {}
        payload['tpid'] = tpid

        headers = {}
        headers['Content-Type'] = 'application/json'

        try:

            moisesResponse = requests.request("POST", url, headers=headers, json=payload)
            logging.warning('RESPONE GET INFO FROM CUSTOMER %s' % (moisesResponse.text))
            moisesResponse = moisesResponse.json()

            if not moisesResponse['result'] == 1:
                respone : get_customer_output_schema = {}
                respone['success'] = False
                respone['message'] = "Customer noit exist"
                respone['payload'] = {}

                return respone

            respone : get_customer_output_schema = {}
            respone['success'] = True
            respone['message'] = "Customer info"
            respone['payload'] = {}
            respone['payload']['tpid'] = moisesResponse['data']['tpId']
            respone['payload']['crmId'] = moisesResponse['data']['crmId']
            respone['payload']['firstName'] = moisesResponse['data']['firstName']
            respone['payload']['lastName'] = moisesResponse['data']['lastName']
            respone['payload']['phoneCode'] = moisesResponse['data']['phoneCode']
            respone['payload']['phoneNumber'] = moisesResponse['data']['phoneNumber']

            return respone
    
        except Exception as Err:
            respone : get_customer_output_schema = {}
            respone['success'] = False
            respone['message'] = str(Err)
            respone['payload'] = {}

            return respone

    