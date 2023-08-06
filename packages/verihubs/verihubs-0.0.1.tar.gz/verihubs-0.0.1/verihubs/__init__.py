import requests


class VeriHubs:

    def __init__(self, app_id: str, api_key: str) -> None:
        self.app_id = app_id
        self.api_key = api_key
        self.base_url = 'https://api.verihubs.com/v1'

    
    @property
    def headers(self):
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }
        headers['App-ID'] = self.app_id
        headers['API-Key'] = self.api_key
        return headers
    

    def send_sms_otp(self, phone: str, template: str = None, expired: int = 300):
        url = self.base_url + '/otp/send'
        payload = {'msidn': phone, 'time_limit': expired}
        if template is None:
            template = 'This is your Verihubs OTP $OTP.'
            payload['template'] = template
        r = requests.post(
            url,
            headers=self.headers,
            json=payload)
        return r
    

    def verify_sms_otp(self, phone: str, otp: str):
        url = self.base_url + '/otp/verify'
        payload = {'msidn': phone, 'otp': otp}
        r = requests.post(
            url,
            headers=self.headers,
            json=payload)
        return r