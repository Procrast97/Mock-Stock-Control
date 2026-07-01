import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from datetime import datetime as dt

load_dotenv()

class Notify:

    SENDER = "Ocledo Alerts <alerts@ocledo.com>"
    SMTP_PORT = 465
    RECIPIENTS = {
        "out_of_stock": ["pyttesting1@gmail.com"],
        "critical": ["pyttesting1@gmail.com", "ocledodev@gmail.com"],
        "low_stock": ["pyttesting1@gmail.com"],
    }
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("base.html")

    def __init__(self, sender_email, password, alias_email, smtp_server):
        self.smtp_email = sender_email
        self.smtp_password = password
        self.alias_email = alias_email
        self.smtp_server = smtp_server
        self.smtp = None

    def __enter__(self):
        self.connection = smtplib.SMTP_SSL(self.smtp_server, self.SMTP_PORT)
        self.connection.login(self.smtp_email, self.smtp_password)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.quit()

    def send_digest(self, oos, cs, ls):
        tiers = [
            ("Out of Stock", oos, self.RECIPIENTS["out_of_stock"], "#c0392b"),
            ("Critical Stock", cs, self.RECIPIENTS["critical"], "#d68910"),
            ("Low Stock", ls, self.RECIPIENTS["low_stock"], "#b7950b"),
        ]

        for tier_name, items, recipients, color in tiers:
            if not items:
                continue #This skips empty tiers completely.

            html_body = self.template.render(
                generated_at=dt.now().strftime("%Y-%m-%d %H:%M"),
                tier_name=tier_name,
                items=items,
                color=color,
            )

            msg = EmailMessage()
            msg["Subject"] = f"{tier_name} Alert - {dt.now().strftime('%d %b %Y')}"
            msg["From"] = self.alias_email
            msg["To"] = ", ".join(recipients)
            msg.set_content("Please enable enable HTML to view this email.")
            msg.add_alternative(html_body, subtype="html")

            self.connection.send_message(msg)
            print(f"{tier_name} alert sent tp: {', '.join(recipients)}")
