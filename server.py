
from flask import Flask, render_template, request
from smtplib import SMTP, SMTPResponseException, SMTPAuthenticationError
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/generic')
def generic():
    return render_template('generic.html')


@app.route('/elements')
def elements():
    return render_template('elements.html')


@app.route('/send_email', methods=["POST"])
def send_email():
    from_email = request.form["email"]
    email_message = request.form["message"]
    user = request.form["name"]
    smtp_email = os.getenv("my_email")
    smtp_pass = os.getenv("password")
    try:
        with SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=smtp_email, password=smtp_pass)
            connection.sendmail(
                from_addr=from_email,
                to_addrs="aboyles05@gmail.com",
                msg=f"Subject: New Inquiry from {user} at {from_email}!\n\n  {email_message}")
    except SMTPResponseException as e:
        error_message = f"Sorry we could not complete the request due to{e.smtp_error}"
        return error_message
    else:
        message = "We will be in touch with you soon, " \
                  "please allow 3 business days for us to respond"
        return render_template("send_email_success.html", result=message)


if __name__ == "__main__":
    app.run(debug=True)


