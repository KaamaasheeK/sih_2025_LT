# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from app.database import get_connection
# import mysql.connector

# router = APIRouter(prefix="/auth", tags=["auth"])

# # --------------------
# # Pydantic models
# # --------------------
# class RegisterRequest(BaseModel):
#     name: str
#     password: str
#     mail: str  # matches the DB column
#     role: str  # new field for role

# class LoginRequest(BaseModel):
#     name: str
#     password: str

# # --------------------
# # Register route
# # --------------------
# @router.post("/register")
# def register(data: RegisterRequest):
#     try:
#         conn = get_connection()
#         cursor = conn.cursor()

#         # Check if name or mail already exists
#         cursor.execute("SELECT * FROM users WHERE name=%s OR mail=%s", (data.name, data.mail))
#         existing = cursor.fetchone()
#         if existing:
#             conn.close()
#             raise HTTPException(status_code=400, detail="Name or mail already exists")

#         # Insert new user with role
#         query = "INSERT INTO users (name, password, mail, role) VALUES (%s, %s, %s, %s)"
#         cursor.execute(query, (data.name, data.password, data.mail, data.role))
#         conn.commit()
#         conn.close()
#         return {"message": "User registered successfully"}

#     except mysql.connector.Error as e:
#         raise HTTPException(status_code=500, detail=f"MySQL Error: {e}")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # --------------------
# # Login route
# # --------------------
# @router.post("/login")
# def login(data: LoginRequest):
#     try:
#         conn = get_connection()
#         cursor = conn.cursor(dictionary=True)

#         query = "SELECT * FROM users WHERE name=%s AND password=%s"
#         cursor.execute(query, (data.name, data.password))
#         user = cursor.fetchone()
#         conn.close()

#         if not user:
#             raise HTTPException(status_code=401, detail="Invalid credentials")
#         return {"message": "Login successful", "user": user}

#     except mysql.connector.Error as e:
#         raise HTTPException(status_code=500, detail=f"MySQL Error: {e}")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import get_connection
import mysql.connector

router = APIRouter(prefix="/auth", tags=["auth"])

# --------------------
# Pydantic models
# --------------------
class RegisterRequest(BaseModel):
    name: str
    mail: str
    password: str
    role: str  # e.g., admin, user, staff

class LoginRequest(BaseModel):
    mail: str
    password: str

# --------------------
# Register route
# --------------------
@router.post("/register")
def register(data: RegisterRequest):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Check if name or mail already exists
        cursor.execute("SELECT * FROM users WHERE name=%s OR mail=%s", (data.name, data.mail))
        existing = cursor.fetchone()
        if existing:
            conn.close()
            raise HTTPException(status_code=400, detail="Name or mail already exists")

        # Insert new user with role
        query = "INSERT INTO users (name, mail, password, role) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (data.name, data.mail, data.password, data.role))
        conn.commit()
        conn.close()
        return {"message": "User registered successfully"}

    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"MySQL Error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --------------------
# Login route
# --------------------
@router.post("/login")
def login(data: LoginRequest):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM users WHERE mail=%s AND password=%s"
        cursor.execute(query, (data.mail, data.password))
        user = cursor.fetchone()
        conn.close()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {"message": "Login successful", "user": user}

    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"MySQL Error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
