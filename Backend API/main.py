from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from datetime import datetime
import pandas as pd
import joblib


# ------------------------------------------------
# 1. APP CONFIGURATION
# ------------------------------------------------
app = FastAPI(
    title="Banff Traffic & Parking AI API",
    description=(
        "FastAPI backend providing traffic predictions for residents and visitors, "
        "plus automated holiday and seasonal event detection."
    ),
    version="1.0.0",
)

# CORS: allows your React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # you may restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent


# ------------------------------------------------
# 2. FILE PATHS & CONSTANTS
# ------------------------------------------------
HOLIDAYS_CSV_PATH = BASE_DIR / "banff_tourism_ml_features.csv"
RESIDENT_MODEL_PATH = BASE_DIR / "models" / "xgb_807_model_resident.joblib"
VISITOR_MODEL_PATH = BASE_DIR / "models" / "xgb_2161_model_visitor.joblib"

# Feature ordering as expected by each model
RESIDENT_FEATURES = [
    "day_of_week_num",
    "hour",
    "WestEntrance_Southbound_lag3",
    "is_holiday_BC",
    "is_holiday_AB",
    "is_holiday_US",
    "rolling_mean_3h",
    "is_bad_weather",
    "month",
    "total_downtown_outflow_lag3",
]

VISITOR_FEATURES = [
    "hour",
    "MountainAve_Southbound_lag3",
    "rolling_std_24h",
    "WestEntrance_Northbound_lag3",
    "target_lag3",
    "day_of_week_num",
    "target_lag24",
]


# ------------------------------------------------
# 3. LOAD HOLIDAYS (CSV → DICTIONARY LOOKUP)
# ------------------------------------------------
def load_holiday_table(csv_path: Path):
    if not csv_path.exists():
        raise RuntimeError(f"Holiday CSV not found at: {csv_path}")

    df = pd.read_csv(csv_path)

    if "date" not in df.columns:
        raise RuntimeError("Holiday CSV must contain a 'date' column.")

    # Ensure date column is parsed correctly
    df["date"] = pd.to_datetime(df["date"]).dt.date

    holiday_lookup = {}

    for _, row in df.iterrows():
        date_obj = row["date"]
        date_str = date_obj.isoformat()

        # Use existing day_of_week column if available
        if "day_of_week" in df.columns:
            day_of_week_num = int(row["day_of_week"])
        else:
            dow = date_obj.weekday()  # 0=Monday, 6=Sunday
            day_of_week_num = dow + 1

        holiday_lookup[date_str] = {
            "day_of_week_num": day_of_week_num,
            "month": int(date_obj.month),
            "is_holiday_AB": int(row.get("is_holiday_AB", 0)),
            "is_holiday_BC": int(row.get("is_holiday_BC", 0)),
            "is_holiday_US": int(row.get("is_holiday_US", 0)),
            "is_spring_break": int(row.get("is_spring_break", 0)),
            "is_stampede": int(row.get("is_stampede", 0)),
        }

    return holiday_lookup


# Load holiday table
try:
    HOLIDAY_TABLE = load_holiday_table(HOLIDAYS_CSV_PATH)
    print(f"Holidays loaded: {len(HOLIDAY_TABLE)} rows.")
except Exception as e:
    print("Error loading holidays:", e)
    HOLIDAY_TABLE = {}


# ------------------------------------------------
# 4. LOAD ML MODELS
# ------------------------------------------------
def load_model(path: Path):
    if not path.exists():
        raise RuntimeError(f"Model not found at: {path}")
    return joblib.load(path)

try:
    resident_model = load_model(RESIDENT_MODEL_PATH)
    print("Resident model loaded.")
except Exception as e:
    print("Error loading resident model:", e)
    resident_model = None

try:
    visitor_model = load_model(VISITOR_MODEL_PATH)
    print("Visitor model loaded.")
except Exception as e:
    print("Error loading visitor model:", e)
    visitor_model = None


# ------------------------------------------------
# 5. Pydantic MODELS (INPUT VALIDATION)
# ------------------------------------------------
class ResidentRequest(BaseModel):
    day_of_week_num: int
    hour: int
    WestEntrance_Southbound_lag3: float
    is_holiday_BC: int
    is_holiday_AB: int
    is_holiday_US: int
    rolling_mean_3h: float
    is_bad_weather: int
    month: int
    total_downtown_outflow_lag3: float


class VisitorRequest(BaseModel):
    hour: int
    MountainAve_Southbound_lag3: float
    rolling_std_24h: float
    WestEntrance_Northbound_lag3: float
    target_lag3: float
    day_of_week_num: int
    target_lag24: float


# ------------------------------------------------
# 6. ENDPOINT: HOLIDAY & DATE INFO
# ------------------------------------------------
@app.get("/holiday-info")
def get_holiday_info(date: str = Query(..., description="Date in YYYY-MM-DD format")):
    """
    Given a date (YYYY-MM-DD), returns:
    - day_of_week_num (1=Monday ... 7=Sunday)
    - month (1–12)
    - is_holiday_AB, is_holiday_BC, is_holiday_US
    - is_spring_break, is_stampede
    """
    try:
        parsed = datetime.fromisoformat(date).date()
        key = parsed.isoformat()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    if key not in HOLIDAY_TABLE:
        raise HTTPException(status_code=404, detail="Date not found in the holiday table.")

    return HOLIDAY_TABLE[key]


# ------------------------------------------------
# 7. ENDPOINT: PREDICT RESIDENT TRAFFIC
# ------------------------------------------------
@app.post("/predict/resident")
def predict_resident(payload: ResidentRequest):
    """
    Predicts resident vehicle volume for Banff.
    """
    if resident_model is None:
        raise HTTPException(status_code=500, detail="Resident model is not loaded.")

    row = [getattr(payload, feat) for feat in RESIDENT_FEATURES]
    df = pd.DataFrame([row], columns=RESIDENT_FEATURES)

    try:
        y_pred = resident_model.predict(df)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error (resident): {e}")

    return {"prediction": float(y_pred)}


# ------------------------------------------------
# 8. ENDPOINT: PREDICT VISITOR TRAFFIC
# ------------------------------------------------
@app.post("/predict/visitor")
def predict_visitor(payload: VisitorRequest):
    """
    Predicts visitor vehicle volume for Banff.
    """
    if visitor_model is None:
        raise HTTPException(status_code=500, detail="Visitor model is not loaded.")

    row = [getattr(payload, feat) for feat in VISITOR_FEATURES]
    df = pd.DataFrame([row], columns=VISITOR_FEATURES)

    try:
        y_pred = visitor_model.predict(df)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error (visitor): {e}")

    return {"prediction": float(y_pred)}


# ------------------------------------------------
# 9. ROOT ENDPOINT
# ------------------------------------------------
@app.get("/")
def root():
    return {"message": "Banff Traffic & Parking AI API is running 🚗🅿️"}
