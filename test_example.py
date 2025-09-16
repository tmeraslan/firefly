# import unittest
# import requests

# BASE_URL = "http://localhost/v1"
# TOKEN = "2bc2729d33f54aa320147058eb7af8af"  # החלף בטוקן שלך

# HEADERS = {
#     "Authorization": f"Bearer {TOKEN}",
#     "Accept": "application/json"
# }

# class TestFireflyAPI(unittest.TestCase):
    
#     def test_get_accounts(self):
#         response = requests.get(f"{BASE_URL}/accounts", headers=HEADERS)
        
#         # בדיקה שהסטטוס תקין
#         self.assertEqual(response.status_code, 200, "Status code is not 200")
        
#         # בדיקה שהפורמט תקין וכולל מפתח בשם 'data'
#         json_data = response.json()
#         self.assertIn("data", json_data, "Response JSON does not contain 'data' key")

#         # הדפסת התוצאה לצרכים זמניים (אפשר להסיר לאחר מכן)
#         print("Accounts data:")
#         for item in json_data["data"]:
#             print(f"- {item.get('attributes', {}).get('name')}")

# if __name__ == "__main__":
#     unittest.main()
