import requests
import sys

try:
    token = sys.argv[1]
except:
    token = input("Enter Token: ")

data = {"token": token}
url = "https://trial-ku.herokuapp.com/notify/"

# url = "http://localhost:8000/notify/"
response = requests.post(url, data)
try:
    js_obj = response.json()
    code = js_obj["status"]
    if code == 403:
        print(js_obj["message"])
        exit()
    elif code == 200:
        print("Success")

    else:
        print("Snap. Some error Occured")

except:
    print("Something is wrong! I can feel it!")
