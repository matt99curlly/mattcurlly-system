from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_risk_info(d1, d2):
    d1, d2 = d1.lower().strip(), d2.lower().strip()
    nsaids = {"aspirin", "ibuprofen", "naproxen"}
    sedatives = {"diphenhydramine", "diazepam", "melatonin", "alcohol"}
    
    if d1 in nsaids and d2 in nsaids:
        return {"risk": "High", "effect": "Increased risk of stomach bleeding.", "rec": "Avoid mixing."}
    if d1 in sedatives and d2 in sedatives:
        return {"risk": "High", "effect": "Severe drowsiness/breathing issues.", "rec": "DANGER: Do not combine."}
    
    return {"risk": "Moderate", "effect": "Potential side effects.", "rec": "Consult a pharmacist."}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/check", response_class=HTMLResponse)
async def check_interaction(request: Request, drug1: str = Form(...), drug2: str = Form(...)):
    result = get_risk_info(drug1, drug2)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "drug1": drug1,
        "drug2": drug2,
        "risk_level": result["risk"],
        "side_effects": result["effect"],
        "recommendation": result["rec"]
    })

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)