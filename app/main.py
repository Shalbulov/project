from fastapi import FastAPI, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, database

# создание таблиц
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return RedirectResponse(url="/login")

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login_submit(username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "password123":
        return RedirectResponse(url="/index", status_code=303)
    return RedirectResponse(url="/login", status_code=303)

@app.get("/index", response_class=HTMLResponse)
def read_index(
    request: Request, 
    db: Session = Depends(get_db),
    search: str = "",
    year: str = "",
    country: str = "",
    rating: str = "",
    category: str = ""
):

    years_query = db.query(models.Film.release_year).distinct().order_by(models.Film.release_year.desc()).all()
    countries_query = db.query(models.Film.country).filter(models.Film.country != None).distinct().order_by(models.Film.country).all()
    ratings_query = db.query(models.Film.rating).filter(models.Film.rating != None).distinct().order_by(models.Film.rating).all()
    categories_query = db.query(models.Film.listed_in).distinct().order_by(models.Film.listed_in).all()

    # основной запрос фильмов
    query = db.query(models.Film)

    # фильтры
    if search:
        query = query.filter(models.Film.title.ilike(f"%{search}%"))
    if year:
        query = query.filter(models.Film.release_year == int(year))
    if country:
        query = query.filter(models.Film.country == country)
    if rating:
        query = query.filter(models.Film.rating == rating)
    if category:
        query = query.filter(models.Film.listed_in == category)

    total_found = query.count()
    films = query.limit(100).all()
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "movies": films,
        "total": total_found,
        "filter_data": {
            "years": [y[0] for y in years_query],
            "countries": [c[0] for c in countries_query],
            "ratings": [r[0] for r in ratings_query],
            "categories": [cat[0] for cat in categories_query]
        },
        "selected": {
            "search": search,
            "year": year,
            "country": country,
            "rating": rating,
            "category": category
        }
    })