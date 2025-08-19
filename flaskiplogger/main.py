from flask import Flask, request, render_template
import datetime, os, requests

app = Flask(__name__)

if not os.path.exists("ip_log.txt"):
    open("ip_log.txt", "w").close()

@app.route('/')
def home():
    if request.headers.getlist("X-Forwarded-For"):
        ip_address = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip_address = request.remote_addr

    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}").json()
        location_info = f"{response.get('city')}, {response.get('regionName')}, {response.get('country')} | ISP: {response.get('isp')}"
    except:
        location_info = "Location lookup failed"

    now = datetime.datetime.now()

    with open("ip_log.txt", "a") as log_file:
        log_file.write(f"{now} - {ip_address} - {location_info}\n")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

