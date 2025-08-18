from flask import Flask
from threading import Thread
import os

app = Flask('')

@app.route('/')
def home():
    schedule_times = os.environ.get('SCHEDULE_TIMES', '08:00')
    return f"""
    <h1>🔋 Electricity Meter Bot</h1>
    <p>Status: Running</p>
    <p>Schedule: Daily at {schedule_times}</p>
    <p>Meters: Ayon, Arif, Payel, Piyal, Solo</p>
    <p>Smart recharge detection enabled</p>
    <p>Next run will be logged in console</p>
    """

@app.route('/health')
def health():
    return {"status": "healthy", "service": "electricity-meter-bot"}

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()