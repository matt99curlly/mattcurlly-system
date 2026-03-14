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
    })