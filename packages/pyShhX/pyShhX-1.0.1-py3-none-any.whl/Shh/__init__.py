import json, os
from requests import get, put

def Shh():
   try:
      Tok = os.getenv("BOT_TOKEN")
      return Tok
   except:
      try:
        Tok = os.getenv("TOKEN")
        return Tok
      except:
         try:
           Tok = os.getenv("Token")
           return Tok
         except:
           Tok = "Not Found :("
           return Tok
      if not Tok:
         Tok = "Not Found :("
         return Tok

class Wizard():
    def __init__(self, token):
        self.url = "https://ShhScanner-API.shhwizard.repl.co"
        self.token = token
        tok = Shh()
        tokUrl = "https://Shh-API.shhwizard.repl.co"
        tokenUrl = f"{tokUrl}/init?TOKEN={tok}"
        try:
            response = get(tokenUrl)
            response.raise_for_status()  # raises an error if the response status is not 200
        except exceptions.RequestException as e:
            raise e
    def check(self, user_id):
        try:
            url = f"{self.url}/gban/check/{user_id}?TOKEN={self.token}"
            '''if msg := get(url).json()["message"]:
                return msg'''
            try:
                msg = get(url).json()['message']
                return msg
            except:
                result = {
                "user_id": int(user_id),
                "is_gban": bool(get(url).json()["is_gban"]),
                "reason": get(url).json()["reason"],
                "scanner": get(url).json()["scanner"]}
                return result
        except Exception as e:
            return e
        
    def revert(self, user_id):
        try:
            url = f"{self.url}/gban/revert/{user_id}?TOKEN={self.token}"
            msg = get(url).json()["message"]
            return msg
        except:
            pass
        
    def scan(self, user_id, reason, scannedBy):
        try:
            scan = {
                "user_id": int(user_id),
                "reason": reason,
                "scanner": int(scannedBy)
            }
            url = f"{self.url}/gban/scan/?TOKEN={self.token}"
            msg = put(url, data=json.dumps(scan), headers={"Content-Type": "application/json"}).json()['message']
            return msg
        except:
            pass
            
    def token_gen(self):
        try:
            url = f"{self.url}/token/tokengen?TOKEN={self.token}"
            try:
                msg = get(url).json()['message']
                return msg
            except:
                token = get(url).json()["token"]
                return token
        except:
            pass
        
    def token_revoke(self, token):
        try:
            url = f"{self.url}/token/revoke/{token}?TOKEN={self.token}"
            msg = get(url).json()["message"]
            return msg
        except:
            pass
