from flask import Flask, request, Response

app = Flask(__name__)

@app.route("/ivr/fraud-alert", methods=["GET", "POST"])
def fraud_alert():
    xml = """
    <Response>
        <Speak>This is URBANK. A suspicious transaction was detected on your account.</Speak>
        <GetDigits timeout="10" numDigits="1" action="https://ivr-flask.onrender.com/ivr/fraud-response" method="POST">
            <Speak>Press 1 to confirm the transaction. Press 2 to report fraud.</Speak>
        </GetDigits>
        <Speak>No input received. Goodbye.</Speak>
        <Hangup/>
    </Response>
    """
    return Response(xml.strip(), mimetype='text/xml')

@app.route("/ivr/fraud-response", methods=["GET", "POST"])
def fraud_response():
    digit = request.values.get("Digits", "")
    msg = {
        "1": "Thank you. The transaction has been confirmed.",
        "2": "Fraud alert recorded. Our team will contact you.",
    }.get(digit, "Invalid input. Goodbye.")
    return Response(f"<Response><Speak>{msg}</Speak><Hangup/></Response>", mimetype='text/xml')

if __name__ == "__main__":
    app.run()
