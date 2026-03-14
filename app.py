<<<<<<< HEAD
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import pandas as pd

app = FastAPI()
# This folder must exist and contain index.html
templates = Jinja2Templates(directory="templates")

def get_drug_list():
    try:
        # Reads your list of drugs from your CSV
        df = pd.read_csv('drugs.csv')
        # Returns a unique, sorted list
        return sorted(df['drug_name'].dropna().unique().tolist())
    except Exception:
        # Fallback if file is missing
        return ["Aspirin", "Ibuprofen", "Warfarin", "Lisinopril"]

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "drugs": get_drug_list()
    })

@app.post("/check_interaction")
def check_interaction(request: Request, drug1: str = Form(...), drug2: str = Form(...)):
    # Add your existing interaction logic here
    result = f"Checking interaction for {drug1} and {drug2}..."
    return templates.TemplateResponse("result.html", {
        "request": request, 
        "result": result
=======
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
# Ensure your 'templates' folder is in the same directory as this file
templates = Jinja2Templates(directory="templates")

def get_risk_info(d1, d2):
    # Normalize inputs
    d1, d2 = d1.lower().strip(), d2.lower().strip()
    
    # Define Drug Categories
    nsaids = {"aspirin", "ibuprofen", "naproxen"}
    sedatives = {"diphenhydramine", "diazepam", "melatonin", "alcohol"}
    
    # Check for High Risk interactions
    if d1 in nsaids and d2 in nsaids:
        return {
            "risk": "High",
            "effect": "Increased risk of stomach bleeding and kidney strain.",
            "rec": "Avoid mixing multiple NSAIDs. Consult a doctor for safer pain management."
        }
    
    if d1 in sedatives and d2 in sedatives:
        return {
            "risk": "High",
            "effect": "Severe drowsiness, impaired coordination, and slowed breathing.",
            "rec": "DANGER: Do not combine these. It can lead to dangerous levels of sedation."
        }
        
    # Default to Moderate Risk
    return {
        "risk": "Moderate",
        "effect": "Potential for unpredictable side effects or reduced drug effectiveness.",
        "rec": "Always consult a pharmacist before combining any medications."
    }

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/check", response_class=HTMLResponse)
async def check_interaction(drug1: str, drug2: str, request: Request):
    result = get_risk_info(drug1, drug2)
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "drug1": drug1, 
        "drug2": drug2,
        "risk_level": result["risk"],
        "side_effects": result["effect"],
        "recommendation": result["rec"]
>>>>>>> de1520ecdfa75f52454b441ed19b555cb03316b6
    })