"""USB serial bridge: ESP32 sends one JSON object per serial line."""
import argparse, json, serial, requests

parser = argparse.ArgumentParser()
parser.add_argument("--port", required=True, help="Example: COM5 on Windows")
parser.add_argument("--baud", type=int, default=115200)
parser.add_argument("--token", required=True)
parser.add_argument("--receiver", default="http://127.0.0.1:8000/telemetry")
args = parser.parse_args()

ser = serial.Serial(args.port, args.baud, timeout=2)
print("NOVACARE USB bridge running. Press Ctrl+C to stop.")
while True:
    line = ser.readline().decode("utf-8", errors="ignore").strip()
    if not line:
        continue
    try:
        payload = json.loads(line)
        response = requests.post(args.receiver, json=payload,
            headers={"X-Device-Token": args.token}, timeout=5)
        print(response.status_code, response.text)
    except Exception as exc:
        print("Skipped serial line:", exc)
