from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
import sqlite3, hashlib
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).with_name("novacare.db")
app = FastAPI(title="NOVACARE Wearable Receiver", version="1.2")

class Telemetry(BaseModel):
    device_id: str
    heart_rate: float | None = Field(default=None, ge=0, le=250)
    spo2: float | None = Field(default=None, ge=0, le=100)
    skin_temp: float | None = Field(default=None, ge=0, le=50)
    respiration: float | None = Field(default=None, ge=0, le=100)
    movement: float | None = Field(default=None, ge=0, le=10000)

@app.get("/health")
def health():
    return {"service": "NOVACARE receiver", "status": "online"}

@app.post("/telemetry")
def telemetry(data: Telemetry, x_device_token: str = Header(default="")):
    if not DB_PATH.exists():
        raise HTTPException(503, "Start NOVACARE dashboard once to create its database.")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    device = conn.execute("SELECT * FROM devices WHERE device_code=?", (data.device_id.upper(),)).fetchone()
    if not device:
        conn.close()
        raise HTTPException(404, "Unknown device ID")
    digest = hashlib.sha256(x_device_token.encode()).hexdigest()
    if not x_device_token or digest != device["secret_hash"]:
        conn.close()
        raise HTTPException(401, "Invalid device token")
    if device["astronaut_id"] is None:
        conn.close()
        raise HTTPException(409, "Assign this wearable to an astronaut in NOVACARE first.")
    now = datetime.now().isoformat(timespec="seconds")
    conn.execute("""INSERT INTO records(astronaut_id,device_code,timestamp,heart_rate,spo2,skin_temp,respiration,movement,source,raw_json)
    VALUES(?,?,?,?,?,?,?,?,?,?)""",
    (device["astronaut_id"], data.device_id.upper(), now, data.heart_rate, data.spo2,
     data.skin_temp, data.respiration, data.movement, "Wearable", data.model_dump_json()))
    conn.execute("UPDATE devices SET status='Connected',last_seen=? WHERE id=?", (now, device["id"]))
    conn.commit()
    conn.close()
    return {"accepted": True, "device_id": data.device_id.upper(), "timestamp": now}
