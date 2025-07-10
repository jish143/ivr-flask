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




@app.route("/greeting", methods=["GET"])
def greeting():
    # You can use request.args.get("customField") if you want dynamic message later
    message = "This is a fraud alert call from URBANK."

    # Exotel expects plain text (not XML or JSON) for dynamic greeting
    return Response(message, mimetype="text/plain")

@app.route("/block", methods=["GET"])
def test():
    # Print all query params to console
    print("Received GET parameters:")
    for key, value in request.args.items():
        print(f"{key} = {value}")

    return "Parameters received", 200

@app.route("/")
def index():
    return "Exotel IVR Flask App Running"


if __name__ == "__main__":
    app.run()
