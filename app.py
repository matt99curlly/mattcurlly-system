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
    })