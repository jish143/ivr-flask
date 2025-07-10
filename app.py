from flask import Flask, request, Response

app = Flask(__name__)

@app.route("/ivr/fraud-alert", methods=["GET", "POST"])
def fraud_alert():
    data = request.args if request.method == "GET" else request.form
    caller = data.get("From")
    called = data.get("To")
    custom_field = data.get("customField", "")

    # Build your dynamic message
    message = f"This is URBANK. We noticed a transaction. Press 1 to confirm, 2 to report fraud."

    xml = f"""
    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say>{message}</Say>
        <Gather action="https://<your-host>/ivr/handle-input" method="POST" numDigits="1" timeout="5" />
    </Response>
    """

    return Response(xml.strip(), mimetype="text/xml")



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
