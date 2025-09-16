# # from fastapi import APIRouter
# # from app.models import MeterData
# # from app.services import meter_service

# # router = APIRouter(prefix="/meters", tags=["Meters"])

# # @router.post("/add")
# # def add_meters(data: MeterData):
# #     meter_service.add_meters_to_db(data)
# #     alerts = meter_service.check_voltage_alerts(data)
# #     return {"status": "success", "alerts": alerts}


# # @router.get("/all")
# # def get_meters():
# #     return meter_service.get_all_meters()
# # from fastapi import APIRouter
# # from typing import List
# # from app.models import Meter, EventOut
# # from app.services import meter_service

# # router = APIRouter(prefix="/meters", tags=["Meters"])

# # @router.post("/", summary="Add or update meter")
# # def add_meter(meter: Meter):
# #     return meter_service.add_meter(meter)

# # @router.get("/", response_model=List[Meter], summary="Get all meters")
# # def get_meters():
# #     return meter_service.get_meters()

# # @router.get("/events", response_model=List[EventOut], summary="Check meter events")
# # def check_events():
# #     return meter_service.check_events()
# from fastapi import APIRouter
# from app.services.meter_service import get_meters, check_events, add_meter

# router = APIRouter(prefix="/meters", tags=["meters"])

# @router.get("/")
# def read_meters():
#     return get_meters()

# @router.get("/events")
# def read_events():
#     return check_events()

# @router.post("/")
# def create_meter(meter: dict):  # or use Meter Pydantic model
#     return add_meter(meter)
# app/routers/meter_router.py
from fastapi import APIRouter, HTTPException
from app.models import Meter
from app.services.meter_service import add_meter, get_meters, delete_meter, check_events

router = APIRouter(prefix="/meters", tags=["meters"])

# ---------------------------
# Add or Update Meter
# ---------------------------
@router.post("/")
def create_meter(meter: Meter):
    try:
        return add_meter(meter)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------
# Get All Meters
# ---------------------------
@router.get("/")
def read_meters():
    try:
        return get_meters()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------
# Delete a Meter
# ---------------------------
@router.delete("/{meter_id}")
def remove_meter(meter_id: str):
    try:
        result = delete_meter(meter_id)
        if "not found" in result["message"]:
            raise HTTPException(status_code=404, detail=result["message"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------
# Get Events (Line Health)
# ---------------------------
@router.get("/events")
def read_events():
    try:
        return check_events()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
