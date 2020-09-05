import http.client
import json

conn = http.client.HTTPSConnection("dev20.auth0.com")
payload = "grant_type=client_credentials&client_id=mu1d1oQSQr9EkkZ9KhkIkZQc21axNZ63&client_secret=DggOB5ORvPQla2ySyqI1P6s6JmnZtcF_VBiBu_M5rtHqsMC_rSt-wRVb_JOeUn62&audience=https://rcommand"
headers = { 'content-type': "application/x-www-form-urlencoded" }
conn.request("POST", "/oauth/token", payload, headers)
res = conn.getresponse()
data = res.read()
token = json.loads(data.decode('utf-8'))['access_token']
print(f'Token: {token}')

# begin verify token

from jose import jwt
from six.moves.urllib.request import urlopen

AUTH0_DOMAIN = 'dev20.auth0.com'
API_AUDIENCE = 'https://rcommand'
ALGORITHMS = ["RS256"]

jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
jwks = json.loads(jsonurl.read())
unverified_header = jwt.get_unverified_header(token)
rsa_key = {}
for key in jwks["keys"]:
    if key["kid"] == unverified_header["kid"]:
        rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
        }

print(key, '\n')


payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://"+AUTH0_DOMAIN+"/")

print(payload)