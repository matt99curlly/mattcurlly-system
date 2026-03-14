from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import pandas as pd

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Helper to load drugs from CSV
def get_drug_list():
    try:
        df = pd.read_csv('drugs.csv')
        return sorted(df['drug_name'].dropna().unique().tolist())
    except Exception:
        return ["Aspirin", "Ibuprofen", "Warfarin", "Lisinopril"]

# Logic for interaction checking
def get_risk_info(d1, d2):
    d1, d2 = d1.lower().strip(), d2.lower().strip()
    nsaids = {"aspirin", "ibuprofen", "naproxen"}
    sedatives = {"diphenhydramine", "diazepam", "melatonin", "alcohol"}
    
    if d1 in nsaids and d2 in nsaids:
        return {"risk": "High", "effect": "Increased risk of stomach bleeding.", "rec": "Avoid mixing."}
    if d1 in sedatives and d2 in sedatives:
        return {"risk": "High", "effect": "Severe drowsiness.", "rec": "DANGER: Do not combine."}
    
    return {"risk": "Moderate", "effect": "Potential side effects.", "rec": "Consult a pharmacist."}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "drugs": get_drug_list()
    })

@app.post("/check", response_class=HTMLResponse)
async def check_interaction(request: Request, drug1: str = Form(...), drug2: str = Form(...)):
    result = get_risk_info(drug1, drug2)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "drugs": get_drug_list(),
        "drug1": drug1,
        "drug2": drug2,
        "risk_level": result["risk"],
        "side_effects": result["effect"],
        "recommendation": result["rec"]
    })