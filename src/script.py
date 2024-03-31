import json
import logging

import module.setup_logging
from module.notify import Sender
from module.scrapping import Extract

# logger = logging.getLogger(__name__)
# logger.info("Starting")

# with open("credentials.json") as f:
#     creds = json.load(f)
# sender = Sender(creds.get('email_address'), creds.get('password'))
# sender.send("karmehdi@hotmail.com", "test")
# print("done")

extract = Extract()
to_scrap = extract.get_links(1, 20)
test = extract.parse_content(to_scrap[0])
print(len(test))

if __name__ == "__main__":
    # main()
    pass
