from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Bond(Base):
    __tablename__ = 'bonds'

    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String)         # "Spain", "Germany", etc.
    name = Column(String)           # "Spain 10-Year Bond Yield"
    yield_pct = Column(Float)       # Rentabilidad actual (ej: 3.205)
    daily_change = Column(Float)    # Variación absoluta (ej: +0.035)
    daily_change_pct = Column(Float) # Variación porcentual (ej: +1.10)
    last_update = Column(DateTime)  # Última hora de cotización
    currency = Column(String)       # EUR, USD, etc.

engine = create_engine('sqlite:///stocks.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
