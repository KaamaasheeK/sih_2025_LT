# # from fastapi import FastAPI
# # from app.routers import meter_router

# # app = FastAPI(title="LT Line Monitoring System")

# # # include router
# # app.include_router(meter_router.router)

# # @app.get("/")
# # def root():
# #     return {"message": "LT Line Monitoring Backend is Running 🚀"}

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.services.meter_service import add_meters_to_db, get_all_meters

# from app.models import MeterData

# app = FastAPI()

# # Allow frontend URL to access backend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:8081"],  # frontend URL
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.post("/meters/add")
# def add_meters(data: MeterData):
#     alerts = add_meters_to_db(data)
#     return {"status": "success", "alerts": alerts}

# @app.get("/alerts")
# def get_alerts():
#     meters = get_all_meters()
#     alert_events = []

#     for i, m in enumerate(meters):
#         if m['Voltage'] < 200:
#             before = meters[i-1] if i > 0 else None
#             after = meters[i+1] if i < len(meters)-1 else None

#             if (before and before['Voltage'] < 200) and (after and after['Voltage'] < 200):
#                 alert_events.append({
#                     "event": f"Line issue near {m['MeterID']}",
#                     "time": m['Timestamp'],
#                     "severity": "High"
#                 })
#             else:
#                 alert_events.append({
#                     "event": f"{m['MeterID']} low voltage",
#                     "time": m['Timestamp'],
#                     "severity": "Medium"
#                 })
#     return alert_events 
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.routers import meter_router

# app = FastAPI(title="LT Line Monitoring API")

# # CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Include routers
# app.include_router(meter_router.router)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import meter_router
  # import auth router
from app import auth    
app = FastAPI(title="LT Line Monitoring API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(meter_router.router)
app.include_router(auth.router)   # include auth routes
