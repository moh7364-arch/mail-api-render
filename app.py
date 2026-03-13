from flask import Flask, request
import os
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

@app.route("/")
def home():
    return "Mail API is running"

@app.route("/send")
def send_mail():
    to_email = request.args.get("to")
    if not to_email:
        return "Missing 'to' parameter", 400

    smtp_host = os.environ.get("SMTP_HOST")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USER")
    smtp_pass = os.environ.get("SMTP_PASS")
    from_email = os.environ.get("FROM_EMAIL")

    if not all([smtp_host, smtp_port, smtp_user, smtp_pass, from_email]):
        return "SMTP environment variables are missing", 500

    msg = EmailMessage()
    msg["Subject"] = "Test Mail from Render"
    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content("Hello, this email was sent from Render via SMTP.")

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        return f"Mail sent to {to_email}"
    except Exception as e:
        return f"Send failed: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
