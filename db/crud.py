from sqlalchemy.orm import Session
from . import models, schemas


def get_tideGauge(db: Session, tideGauge_id: int):
    return db.query(models.TideGauge).filter(models.TideGauge.id == tideGauge_id).first()


def get_tideGauge_by_name(db: Session, name: str):
    return db.query(models.TideGauge).filter(models.TideGauge.name == name).first()

def get_tideGauge_by_id(db: Session, id: int):
    return db.query(models.TideGauge).filter(models.TideGauge.id == id).first()


def get_tideGauges(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TideGauge).offset(skip).limit(limit).all()


def create_tideGauge(db: Session, tideGauge: schemas.TideGaugeCreate):
    db_tideGauge = models.TideGauge(
        name = tideGauge.name,
        lat = tideGauge.lat,
        lon = tideGauge.lon
    )
    db.add(db_tideGauge)
    db.commit()
    db.refresh(db_tideGauge)
    return db_tideGauge


def create_tideData(db: Session, data: schemas.TideDataCreate, tideGauge_id: int):
    db_data = models.TideData(**data.dict(), tideGauge_id=tideGauge_id)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def get_tideData(db: Session, tideGauge_id):
    return db.query(models.TideData).filter_by(tideGauge_id=tideGauge_id).all()

