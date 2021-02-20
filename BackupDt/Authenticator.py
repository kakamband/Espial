import requests
from getpass import getpass
import json
class Authenticate():
    def __init__(self):
        pass

    def login(self):
        uname = input("Username : ")
        pwd = getpass()
        data = {"username": uname, "password": pwd}
        # url = "https://trial-ku.herokuapp.com/accounts/token/"
        url = "http://localhost:8000/accounts/token/"
        response = requests.post(url, data)
        try:
            js_obj = response.json()
            self.code = js_obj["status"]
            if self.code == 403:
                print(js_obj["message"])
                return 403 
            elif self.code == 200:
                self.token =js_obj["token"]
                return 200
            
            print("Snap. Some error Occured")
            return -1

        except:
            return -1

    def getToken(self):
        if self.code == 200:
            return self.code

        return None