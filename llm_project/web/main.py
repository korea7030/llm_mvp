from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from llm_project.langgraph_app import app as graph_app
from llm_project.display_results import display_results  # HTML 반환 버전으로 수정 필요

fastapi_app = FastAPI()
templates = Jinja2Templates(directory="llm_project/web/templates")
fastapi_app.mount("/static", StaticFiles(directory="llm_project/web/static"), name="static")


@fastapi_app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@fastapi_app.post("/search", response_class=HTMLResponse)
async def search(request: Request, query: str = Form(...)):
    result = graph_app.invoke({"input": query})
    
    layout_type = result.get("layout", "raw")
    # hits = [(hit["user_name"], hit["document"]) for hit in result["hits"]]  # 수정됨
    hits = [
        (meta["user_name"], meta["timestamp"], meta["channel"], doc)
        for doc, meta in result["hits"]
    ]
    highlight_terms = result.get("query", "").split()

    rendered_html = display_results(hits, layout_type=layout_type, highlight_terms=highlight_terms)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "query": query,
        "results_html": rendered_html,
        "layout_type": layout_type,
        "search_type": result.get("search_type", "unknown")
    })