import unittest
import uuid
import requests
import random
import string
from tests.firefly_credentials import get_firefly_credentials


TOKEN = get_firefly_credentials()["token"]
BASE_URL = get_firefly_credentials()["base_url"]

UPDATE_URL = f"{BASE_URL + '/api/v1/accounts'}/{{id}}"
CREATE_ACCOUNT_URL = BASE_URL + "/api/v1/accounts"

def get_headers():
    return {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Trace-Id": str(uuid.uuid4())
    }

class TestUpdateAccountAPI(unittest.TestCase):

    def generate_payload(self, name=None, notes="Test update"):
        return {
            "name": name or f"My checking account {uuid.uuid4()}",
            "type": "asset",
            "account_role": "defaultAsset",
            "currency_id": "1",
            "notes": notes,
            "active": True
        }

    def create_account(self):
        payload = self.generate_payload()
        response = requests.post(CREATE_ACCOUNT_URL, headers=get_headers(), json=payload)
        self.assertEqual(response.status_code, 200, msg=response.text)
        return response.json()["data"]["id"]

    def test_update_account_success(self):
        account_id = self.create_account()
        update_url = UPDATE_URL.format(id=account_id)

        updated_name = "Updated name " + ''.join(random.choices(string.ascii_letters, k=5))
        payload = self.generate_payload(name=updated_name)

        response = requests.put(update_url, headers=get_headers(), json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn(updated_name, response.text)

    def test_update_account_not_found(self):
        fake_id = "999999999"
        update_url = UPDATE_URL.format(id=fake_id)
        payload = self.generate_payload()

        response = requests.put(update_url, headers=get_headers(), json=payload)
        self.assertEqual(response.status_code, 404)


    def test_update_account_missing_auth(self):
        account_id = self.create_account()
        update_url = UPDATE_URL.format(id=account_id)
        headers = get_headers()
        headers.pop("Authorization")
        updated_name = "Updated name " + ''.join(random.choices(string.ascii_letters, k=5))
        payload = self.generate_payload(name=updated_name)
        response = requests.put(update_url, headers=headers, json=payload)
        self.assertEqual(response.status_code, 401)




 
if __name__ == "__main__":
    unittest.main()
