from fastapi import FastAPI
from paho.mqtt import client as mqtt_client
import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# from twilio.rest import Client   # Uncomment if using Twilio SMS

app = FastAPI(title="Line Monitoring Backend")

# -------------------------------
# HiveMQ Cloud MQTT Config
# -------------------------------
BROKER = "a3b15814751f4c2f95b608277e11cd21.s1.eu.hivemq.cloud"
PORT = 8883  # TLS
USERNAME = "Harshan_R"
PASSWORD = "your-password"
TOPIC_STATUS = "harshan/line/status"
TOPIC_RELAY = "harshan/relay"

mqtt_client_id = "backend-service"
mqtt_client = mqtt_client.Client(mqtt_client_id)
mqtt_client.username_pw_set(USERNAME, PASSWORD)
mqtt_client.tls_set(cert_reqs=ssl.CERT_REQUIRED)

# -------------------------------
# Email Config (SMTP Example)
# -------------------------------
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = "your-email@gmail.com"
EMAIL_PASS = "your-app-password"   # App password, not normal login
ALERT_RECEIVER = "lineman@example.com"

def send_email_alert(message: str):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = ALERT_RECEIVER
    msg["Subject"] = "⚡ Line Breakage Alert"
    msg.attach(MIMEText(message, "plain"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, ALERT_RECEIVER, msg.as_string())
    print(f"📧 Alert email sent to {ALERT_RECEIVER}")

# -------------------------------
# Twilio SMS Config (Optional)
# -------------------------------
# TWILIO_SID = "your-twilio-sid"
# TWILIO_AUTH = "your-twilio-auth"
# TWILIO_PHONE = "+1234567890"
# LINEMAN_PHONE = "+919876543210"
#
# def send_sms_alert(message: str):
#     client = Client(TWILIO_SID, TWILIO_AUTH)
#     client.messages.create(
#         body=message,
#         from_=TWILIO_PHONE,
#         to=LINEMAN_PHONE
#     )
#     print(f"📱 SMS alert sent to {LINEMAN_PHONE}")

# -------------------------------
# MQTT Callbacks
# -------------------------------
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Backend connected to HiveMQ")
        client.subscribe(TOPIC_STATUS)
    else:
        print("❌ MQTT Connection failed")

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"📩 Message from {msg.topic}: {payload}")

    if msg.topic == TOPIC_STATUS and payload == "BREAKAGE":
        # Send alert
        alert_msg = "⚡ Line Breakage Detected! Relay switched OFF automatically."
        send_email_alert(alert_msg)
        # send_sms_alert(alert_msg)  # If Twilio enabled

        # Trigger relay OFF
        client.publish(TOPIC_RELAY, "OFF")
        print("🔌 Relay OFF command sent")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Run MQTT loop in background
mqtt_client.connect(BROKER, PORT)
mqtt_client.loop_start()

# -------------------------------
# FastAPI Routes
# -------------------------------
@app.get("/")
def home():
    return {"status": "Backend running, MQTT connected"}

@app.post("/relay/{state}")
def manual_relay_control(state: str):
    if state.upper() in ["ON", "OFF"]:
        mqtt_client.publish(TOPIC_RELAY, state.upper())
        return {"message": f"Relay {state.upper()} command sent"}
    return {"error": "Invalid state. Use ON or OFF"}
