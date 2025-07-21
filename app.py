from flask import Flask, request, render_template
import requests
import time

app = Flask(__name__)

NGL_API_URL = "https://ngl.link/api/submit"

def send_message(ngl_id, message, device_id=None):
    if device_id is None:
        device_id = "device-" + str(time.time()).replace(".", "")
    payload = {
        "username": ngl_id,
        "question": message,
        "deviceId": device_id
    }
    response = requests.post(NGL_API_URL, data=payload)
    return response.status_code == 200

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        ngl_id = request.form["ngl_id"]
        message = request.form["message"]
        count = int(request.form["count"])
        successes = 0
        for i in range(count):
            ok = send_message(ngl_id, f"{message} #{i+1}")
            if ok:
                successes += 1
            time.sleep(0.5)  # small delay to be polite
        result = f"Sent {successes}/{count} messages successfully."
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
