
# from app.database import get_connection
# from app.models import Meter
# from typing import List, Dict

# def add_meter(meter: Meter):
#     conn = get_connection()
#     cur = conn.cursor()
#     sql = """
#     INSERT INTO meters (MeterID, Phase, Voltage, Current, kWh, Event, Latitude, Longitude)
#     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#     ON DUPLICATE KEY UPDATE
#         Phase=VALUES(Phase),
#         Voltage=VALUES(Voltage),
#         Current=VALUES(Current),
#         kWh=VALUES(kWh),
#         Event=VALUES(Event),
#         Latitude=VALUES(Latitude),
#         Longitude=VALUES(Longitude)
#     """
#     cur.execute(sql, (meter.MeterID, meter.Phase, meter.Voltage, meter.Current,
#                       meter.kWh, meter.Event, meter.Latitude, meter.Longitude))
#     conn.commit()
#     conn.close()
#     return {"message": "Meter saved successfully"}

# def get_meters() -> List[Dict]:
#     conn = get_connection()
#     cur = conn.cursor(dictionary=True)
#     cur.execute("SELECT * FROM meters ORDER BY id ASC")
#     rows = cur.fetchall()
#     conn.close()
#     return rows

# def check_events():
#     meters = get_meters()
#     events = []
#     for i, m in enumerate(meters):
#         status = "Normal"
#         if m["Voltage"] < 200:
#             status = "Low Voltage"
#             # check previous and next meter
#             if i > 0 and i < len(meters) - 1:
#                 if meters[i-1]["Voltage"] < 200 and meters[i+1]["Voltage"] < 200:
#                     status = "Whole Line Low Voltage"
#         events.append({
#             "MeterID": m["MeterID"],
#             "Voltage": m["Voltage"],
#             "Status": status
#         })
#     return events
# app/meter_service.py
from app.database import get_connection
from app.models import Meter
from typing import List, Dict

# ---------------------------
# Add or Update Meter
# ---------------------------
def add_meter(meter: Meter):
    conn = get_connection()
    cur = conn.cursor()
    sql = """
    INSERT INTO meters (MeterID, Phase, Voltage, Current, kWh, Event, Latitude, Longitude)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        Phase=VALUES(Phase),
        Voltage=VALUES(Voltage),
        Current=VALUES(Current),
        kWh=VALUES(kWh),
        Event=VALUES(Event),
        Latitude=VALUES(Latitude),
        Longitude=VALUES(Longitude)
    """
    cur.execute(sql, (meter.MeterID, meter.Phase, meter.Voltage, meter.Current,
                      meter.kWh, meter.Event, meter.Latitude, meter.Longitude))
    conn.commit()
    conn.close()
    return {"message": f"Meter {meter.MeterID} saved successfully"}

# ---------------------------
# Get All Meters
# ---------------------------
def get_meters() -> List[Dict]:
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM meters ORDER BY id ASC")
    rows = cur.fetchall()
    conn.close()
    return rows

# ---------------------------
# Delete a Meter
# ---------------------------
def delete_meter(meter_id: str) -> Dict:
    conn = get_connection()
    cur = conn.cursor()
    sql = "DELETE FROM meters WHERE MeterID = %s"
    cur.execute(sql, (meter_id,))
    conn.commit()
    conn.close()

    if cur.rowcount == 0:
        return {"message": f"Meter {meter_id} not found"}
    return {"message": f"Meter {meter_id} deleted successfully"}

# ---------------------------
# Check Events (Line Status)
# ---------------------------
def check_events() -> List[Dict]:
    meters = get_meters()
    events = []
    for i, m in enumerate(meters):
        status = "Normal"
        if m["Voltage"] < 200:
            status = "Low Voltage"
            # check previous and next meter
            if i > 0 and i < len(meters) - 1:
                if meters[i-1]["Voltage"] < 200 and meters[i+1]["Voltage"] < 200:
                    status = "Whole Line Low Voltage"
        events.append({
            "MeterID": m["MeterID"],
            "Voltage": m["Voltage"],
            "Status": status
        })
    return events
