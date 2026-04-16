from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer


# 🔐 DATABASE
from pymongo import MongoClient
from passlib.context import CryptContext

# ================= INIT =================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= DB =================
client = MongoClient("mongodb://localhost:27017/")
db = client["bgd_db"]

users = db["users"]
history = db["history"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ================= MODEL =================
model = load_model("model.h5")
classes = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

# ================= IMAGE PROCESS =================
def preprocess_image(file_bytes):
    nparr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# ================= AUTH =================

@app.post("/register")
async def register(username: str, password: str):
    if users.find_one({"username": username}):
        return {"status": "error", "message": "User already exists"}

    hashed = pwd_context.hash(password)
    users.insert_one({"username": username, "password": hashed})

    return {"status": "success", "message": "User registered"}

@app.post("/login")
async def login(username: str, password: str):
    user = users.find_one({"username": username})

    if not user:
        return {"status": "error", "message": "User not found"}

    if not pwd_context.verify(password, user["password"]):
        return {"status": "error", "message": "Wrong password"}

    return {"status": "success", "message": "Login successful"}

# ================= PREDICT =================

@app.post("/predict")
async def predict(file: UploadFile = File(...), username: str = ""):
    try:
        contents = await file.read()
        image = preprocess_image(contents)

        prediction = model.predict(image)
        result = classes[np.argmax(prediction)]

        # Save history
        if username:
            history.insert_one({
                "username": username,
                "blood_group": result
            })

        return {
            "status": "success",
            "blood_group": result
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

# ================= HISTORY =================

@app.get("/history")
def get_history(username: str):
    data = list(history.find({"username": username}, {"_id": 0}))
    return data

# ================= ADMIN =================

@app.get("/all-results")
def all_results():
    data = list(history.find({}, {"_id": 0}))
    return data

# ================= ROOT =================

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1>🧠 AI Fingerprint Blood Group Detection</h1>
    <p>Backend is running successfully 🚀</p>
    <a href="/docs">👉 Open API Docs</a> 
    """




