from flask import Flask, request, Response

app = Flask(__name__)

@app.route("/ivr/fraud-alert", methods=["POST"])
def fraud_alert():
    custom_field = request.form.get("customField", "")

    # Parse example: txn_id=TXN123&amount=10000&type=UPI
    info = dict(item.split("=") for item in custom_field.split("&") if "=" in item)
    amount = info.get("amount", "an unknown amount")
    txn_type = info.get("type", "a transaction")

    message = f"This is URBANK. We noticed a {txn_type} of rupees {amount}. Press 1 to confirm, 2 to report fraud."

    response = f"""
    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say>{message}</Say>
        <Gather action="https://ivr-flask.onrender.com/ivr/handle-input" method="POST" numDigits="1" timeout="5" />
    </Response>
    """

    return Response(response.strip(), mimetype="text/xml")


@app.route("/ivr/handle-input", methods=["POST"])
def handle_input():
    digit = request.form.get("Digits")
    if digit == "1":
        say = "Thank you. Your transaction has been confirmed."
    elif digit == "2":
        say = "We have reported this transaction as fraud. Our team will contact you shortly."
    else:
        say = "Invalid input. Goodbye."

    response = f"""
    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say>{say}</Say>
        <Hangup/>
    </Response>
    """

    return Response(response.strip(), mimetype="text/xml")


@app.route("/")
def index():
    return "Exotel IVR Flask App Running"


if __name__ == "__main__":
    app.run()
