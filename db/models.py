from sqlalchemy import Column, ForeignKey, Integer, String, Float
# from sqlalchemy.orm import relationship

from .database import Base


class TideGauge(Base):
    __tablename__ = "tideGauge"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    lat = Column(Float)
    lon = Column(Float)



class TideData(Base):
    __tablename__ = "tideData"

    id = Column(Integer, primary_key=True, index=True)
    timeStamp = Column(Integer, index=True)
    temp = Column(Float)
    nivel = Column(Float)
    tideGauge_id = Column(Integer, ForeignKey("tideGauge.id"))
