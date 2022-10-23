from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from db import crud, models, schemas
from db.database import SessionLocal, engine
from plots.maps import dataGraphs, rjMap

models.Base.metadata.create_all(bind=engine)

#############################
from typing import List
#############################

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/updateimgs')
def updateImages(db: Session = Depends(get_db)):
    tideGauges = crud.get_tideGauges(db=db)
    rjMap(tideGauges)
    for tide in tideGauges:
        dataGraphs(crud.get_tideData(db=db, tideGauge_id=tide.id))
    

    return 'imagens atualizadas'


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    
    with open('plots/mapa.txt', 'r') as f:
        fig = f.read()

    return templates.TemplateResponse('home.html', context={'request':request, 'fig':fig})


@app.get('/tideGauge{id}', response_class=HTMLResponse)
def showTideGauge(request: Request, id, db: Session = Depends(get_db)):
    tideGauge = crud.get_tideGauge_by_id(db, id)
    name = tideGauge.name
    with open(f'plots/tide{id}.txt', 'r') as f:
        tideGraph = f.read()
    
    with open(f'plots/temp{id}.txt', 'r') as f:
        tempGraph = f.read()

    return templates.TemplateResponse(
                f'tideGauge.html',
                context={
                    'request': request,
                    'name': name,
                    'tempGraph': tempGraph,
                    'tideGraph': tideGraph,
                },
            )


@app.post("/createNewTideGauge/", response_model=schemas.TideGauge)
def createTideGauge(tideGauge: schemas.TideGaugeCreate, db: Session = Depends(get_db)):
    db_tideGauge = crud.get_tideGauge_by_name(db, name=tideGauge.name)
    if db_tideGauge:
        raise HTTPException(status_code=400, detail="name already registered")
    return crud.create_tideGauge(db=db, tideGauge=tideGauge)


@app.post("/tideGauge/{tideGauge_id}/data/", response_model=schemas.Tide)
def create_data_for_tideGauge(
    tideGauge_id: int,
    data: schemas.TideDataCreate,
    db: Session = Depends(get_db),
):
    return crud.create_tideData(db=db, data=data, tideGauge_id=tideGauge_id)


@app.get("/TideData/{tideGauge_id}", response_model=List[schemas.Tide])
def read_tideData(tideGauge_id: int, db: Session = Depends(get_db)):
    items = crud.get_tideData(db, tideGauge_id=tideGauge_id)
    return items
