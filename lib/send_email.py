import requests
import json

brevo_api_key = ''

headers = {
    'accept': 'application/json',
    'api-key': brevo_api_key,
    'content-type': 'application/json',
}

data = {
   "sender": {
      "name": "Matej Korbar",
      "email": "matej.korbar@gmail.com"
   },
   "to": [
      {
         "email": "neza.vizintin@yahoo.com",
      }
   ],
   "subject": "Hello world",
   "htmlContent": """
<html>
<head></head>
<body>
<p>Hello,</p>This is my first transactional email sent from Brevo.</p>
</body>
</html>
"""
}


response = requests.post(url='https://api.brevo.com/v3/smtp/email', headers=headers, data=json.dumps(data))

print(response.status_code)
print(response.headers)
print(response.text)
