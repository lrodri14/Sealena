# This file contains all the utilities used to create, edit and remove products or plans from Sealena's Paypal accout

import requests
from Sealena.settings import PAYPAL_ACCESS_TOKEN, PAYPAL_CLIENT_ID, PAYPAL_SECRET_KEY, PAYPAL_AUTH_TOKEN_REQ_ENDPOINT, \
                             PAYPAL_CREATE_PRODUCT_ENDPOINT, PAYPAL_CREATE_PLAN_ENDPOINT, PAYPAL_CANCEL_SUBSCRIPTION_ENDPOINT


def request_access_token():
    """
        DOCSTRING: This request_access_token function is used to request access tokens to the PayPal server, the response
        comes in JSON format, we extract the access token and return it for further use.
    """
    url = PAYPAL_AUTH_TOKEN_REQ_ENDPOINT
    headers = {
        'Content-Type': 'application/json',
        'Accept-Language': 'en_US',
    }
    data = {'grant_type': 'client_credentials'}
    response = requests.request('POST', url, headers=headers, data=data, auth=(PAYPAL_CLIENT_ID, PAYPAL_SECRET_KEY)).json()
    return response['access_token']


def create_product(product_name_id, product_name, description, product_type, category):
    """
        DOCSTRING:
        This create_product function will make a request to the PayPal API whenever a new product needs to be created,
        it expects five parameters from the Product Model, the response information will be used to fill the remaining
        blank fields from the product currently being created.
    """
    url = PAYPAL_CREATE_PRODUCT_ENDPOINT

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(request_access_token()),
        'PayPal-Request-Id': product_name_id
    }

    data = {
        'name': product_name,
        'description': description,
        'type': product_type,
        'category': category
    }

    response = requests.request('POST', url, headers=headers, json=data).json()
    return response


def create_plan(product_id, name_id, name, description, status, frequency, price, tenure, sequence, total_cycles,
                auto_billing, setup_fee, setup_fee_failure_action, payment_failure_threshold):
    """
        DOCSTRING: This create_plan function will make a request to the PayPal API whenever a new
        Plan needs to be created, it expects Plan attributes as parameters to create the Plan, the
        response contains information that will be used to fill the remaining fields from the Plan
        being created.
    """
    url = PAYPAL_CREATE_PLAN_ENDPOINT

    headers = {
        'Authorization': 'Bearer {}'.format(request_access_token()),
        'Content-Type': 'application/json',
        'Paypal-Request-Id': name_id,
    }

    data = {
        'product_id': product_id,
        'name': name,
        'status': status,
        'description': description,
        'billing_cycles': [
            {
                'frequency': {
                    'interval_unit': frequency,
                    'interval_count': 1,
                },
                'pricing_scheme': {
                    'fixed_price': {
                        'currency_code': 'USD',
                        'value': price
                    }
                },
                'tenure_type': tenure,
                'sequence': sequence,
                'total_cycles': total_cycles,
            }
        ],
        'payment_preferences': {
            'auto_bill_outstanding': auto_billing,
            'setup_fee': {
                'currency_code': 'USD',
                'value': setup_fee
            },
            'setup_fee_failure_action': setup_fee_failure_action,
            'payment_failure_threshold': payment_failure_threshold
        },
        'taxes': {
            'percentage': '15',
            'inclusive': True,
        }
    }

    response = requests.request('POST', url, headers=headers, json=data).json()
    return response


def cancel_subscription(subscription_id, reason='/'):
    """
        DOCSTRING:
        The cancel_subscription function will be used to unsubscribe a specific user from a plan using the
        PayPal API.
    """
    url = PAYPAL_CANCEL_SUBSCRIPTION_ENDPOINT.format(subscription_id)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(request_access_token())
    }
    data = {
        'reason': reason
    }
    response = requests.request('POST', url, headers=headers, json=data)
    return response

