
import version

VERSION = version.VERSION
__version__ = VERSION

import requests
import auth

from marketo.wrapper import get_lead, get_lead_activity, request_campaign, sync_lead


class Client:

    def __init__(self, soap_endpoint=None, user_id=None, encryption_key=None):

        if not soap_endpoint or not isinstance(soap_endpoint, str):
            raise ValueError('Must supply a soap_endpoint as a non empty string.')

        if not user_id or not isinstance(user_id, str):
            raise ValueError('Must supply a user_id as a non empty string.')

        if not encryption_key or not isinstance(encryption_key, str):
            raise ValueError('Must supply a encryption_key as a non empty string.')

        self.soap_endpoint = soap_endpoint
        self.user_id = user_id
        self.encryption_key = encryption_key

    def wrap(self, body):
        return (
            '<?xml version="1.0" encoding="UTF-8"?>' +
            '<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"' +
                          'xmlns:ns1="http://www.marketo.com/mktows/" ' +
                          'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '+
                auth.header(self.user_id, self.encryption_key) +
                '<SOAP-ENV:Body>' +
                    body +
                '</SOAP-ENV:Body>' +
            '</SOAP-ENV:Envelope>')

    def request(self, body):
        envelope = self.wrap(body)
        response = requests.post(self.soap_endpoint, data=envelope,
            headers={
                'Connection': 'Keep-Alive',
                'Soapaction': '',
                'Content-Type': 'text/xml;charset=UTF-8',
                'Accept': '*/*'})

        return response

    def get_lead(self, email=None):

        if not email or not isinstance(email, str):
            raise ValueError('Must supply an email as a non empty string.')

        body = get_lead.wrap(email)
        response = self.request(body)
        if response.status_code == 200:
            return get_lead.unwrap(response)
        else:
            raise Exception(response.text)

    def get_lead_activity(self, email=None, filters=[]):

        if not email or not isinstance(email, str):
            raise ValueError('Must supply an email as a non empty string.')

        body = get_lead_activity.wrap(email, filters)
        response = self.request(body)
        if response.status_code == 200:
            return get_lead_activity.unwrap(response)
        else:
            raise Exception(response.text)

    def request_campaign(self, campaign=None, lead=None):

        if not campaign or not isinstance(campaign, str):
            raise ValueError('Must supply campaign id as a non empty string.')

        if not lead or not isinstance(lead, str):
            raise ValueError('Must supply lead id as a non empty string.')

        body = request_campaign.wrap(campaign, lead)

        response = self.request(body)
        if response.status_code == 200:
            return True
        else:
            raise Exception(response.text)

    def sync_lead(self, email=None, attributes=None):

        if not email or not isinstance(email, str):
            raise ValueError('Must supply lead id as a non empty string.')

        if not attributes or not isinstance(attributes, tuple):
            raise ValueError('Must supply attributes as a non empty tuple.')

        body = sync_lead.wrap(email, attributes)

        response = self.request(body)
        if response.status_code == 200:
            return sync_lead.unwrap(response)
        else:
            raise Exception(response.text)
