# from pydantic import BaseModel
# from typing import List

# class Meter(BaseModel):
#     MeterID: str
#     Phase: str
#     Voltage: float
#     Current: float
#     kWh: float
#     Event: str

# class MeterData(BaseModel):
#     DCU_ID: str
#     Timestamp: str
#     Meters: List[Meter]
from pydantic import BaseModel, Field
from typing import Optional

class Meter(BaseModel):
    MeterID: str = Field(..., example="SM12345678")
    Phase: str = Field(..., example="R")
    Voltage: float = Field(..., example=229.0)
    Current: float = Field(..., example=5.2)
    kWh: float = Field(..., example=1542.6)
    Event: Optional[str] = Field("Normal")
    Latitude: float = Field(..., example=12.9716)
    Longitude: float = Field(..., example=77.5946)

class EventOut(BaseModel):
    MeterID: str
    Voltage: float
    Status: str
class UserRegister(BaseModel):
    name: str
    mail: str
    password: str
    role: str = "USER"

class UserLogin(BaseModel):
    mail: str
    password: str