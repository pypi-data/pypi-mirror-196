import unittest
from verihubs import VeriHubs


class BasicsTestCase(unittest.TestCase):

    def test_wrong_app_id(self):
        v = VeriHubs(app_id='something', api_key='something')
        response = v.send_sms_otp('6281310591512')
        self.assertEqual(response.status_code, 401)

    def test_true_app_id(self):
        v = VeriHubs(app_id='something', api_key='something')
        response = v.send_sms_otp('6281310591512')
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()