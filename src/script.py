from module.notify import Sender
import json


with open("credentials.json") as f:
    creds = json.load(f)

sender = Sender(creds.get('email_address'), creds.get('password'))
sender.send("karmehdi@hotmail.com","test")

if __name__ == "__main__":
    # main()
    pass
