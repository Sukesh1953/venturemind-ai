from fastapi import FastAPI
from pydantic import BaseModel

from agents.supervisor import venturemind_graph

app = FastAPI(
    title="VentureMind AI",
    description="Multi-Agent Startup Due Diligence Platform",
    version="1.0.0"
)


class AnalyzeRequest(BaseModel):
    website_url: str
    company_name: str


@app.get("/")
def home():
    return {
        "message": "Welcome to VentureMind AI 🚀"
    }


from fastapi import FastAPI
from pydantic import BaseModel

from agents.supervisor import venturemind_graph

app = FastAPI(
    title="VentureMind AI",
    description="Multi-Agent Startup Due Diligence Platform",
    version="1.0.0"
)


class AnalyzeRequest(BaseModel):
    website_url: str
    company_name: str


@app.get("/")
def home():
    return {
        "message": "Welcome to VentureMind AI 🚀"
    }


@app.post("/analyze")
def analyze(request: AnalyzeRequest):

    result = venturemind_graph.invoke(
        {
            "website_url": request.website_url,
            "company_name": request.company_name
        }
    )

    return {
        "research": result.get("research", ""),
        "business_analysis": result.get("business_analysis", ""),
        "investment_score": result.get("investment_score", ""),
        "market_analysis": result.get("market_analysis", ""),
        "risk_analysis": result.get("risk_analysis", ""),
        "competitors": result.get("competitors", ""),
        "report": result.get("report", "")
    }