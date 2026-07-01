import os
from dotenv import load_dotenv
from DataManager import DataManager
from Notifier import Notify
import time

load_dotenv()
dm = DataManager(os.getenv("FILE_PATH"))

system_active = True

while system_active:
    with Notify(
        sender_email=os.getenv("REAL_EMAIL"),
        password=os.getenv("REAL_PASSWORD"),
        alias_email=os.getenv("ALIAS_EMAIL"),
        smtp_server=os.getenv("SMTP_SERVER"),
    ) as notifier:
        notifier.send_digest(
            oos=dm.out_of_stock(),
            ls=dm.low_stock(),
            cs=dm.critical_stock(),
        )

    time.sleep(30)

