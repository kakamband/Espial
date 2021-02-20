from Authenticator import Authenticate
import requests

auth = Authenticate()
status = auth.login()
if status == 403:
    exit()

elif status == 200:
    data = {"token": auth.getToken(), "head": "TestNotification", "body": "Just a Test"}
    # url = "https://trial-ku.herokuapp.com/accounts/token/"
    url = "http://localhost:8000/notify/"
    response = requests.post(url, data)
    # try:
    js_obj = response.json()
    code = js_obj["status"]
    if code == 403:
        print(js_obj["message"])
        exit() 
    elif code == 200:
        self.token =js_obj["token"]
    
    print("Snap. Some error Occured")

    # except:
    print("Something is wrong! I can feel it!")