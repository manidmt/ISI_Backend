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


bonds_urls = {
    "SPAIN": [
        "https://www.investing.com/rates-bonds/spain-30-year-bond-yield",
        "https://www.investing.com/rates-bonds/spain-20-year-bond-yield",
        "https://www.investing.com/rates-bonds/spain-10-year-bond-yield",
        "https://www.investing.com/rates-bonds/spain-5-year-bond-yield",
        "https://www.investing.com/rates-bonds/spain-2-year-bond-yield",
        "https://www.investing.com/rates-bonds/spain-1-year-bond-yield"
    ],

    "GERMANY": [
        "https://www.investing.com/rates-bonds/germany-30-year-bond-yield",
        "https://www.investing.com/rates-bonds/germany-20-year-bond-yield",
        "https://www.investing.com/rates-bonds/germany-10-year-bond-yield",
        "https://www.investing.com/rates-bonds/germany-5-year-bond-yield",
        "https://www.investing.com/rates-bonds/germany-2-year-bond-yield",
        "https://www.investing.com/rates-bonds/germany-1-year-bond-yield"
    ],

    "USA": [
        "https://www.investing.com/rates-bonds/u.s.-30-year-bond-yield",
        "https://www.investing.com/rates-bonds/u.s.-20-year-bond-yield",
        "https://www.investing.com/rates-bonds/u.s.-10-year-bond-yield",
        "https://www.investing.com/rates-bonds/u.s.-5-year-bond-yield",
        "https://www.investing.com/rates-bonds/u.s.-2-year-bond-yield",
        "https://www.investing.com/rates-bonds/u.s.-1-year-bond-yield"
    ],

    "FRANCE": [
        "https://www.investing.com/rates-bonds/france-30-year-bond-yield",
        "https://www.investing.com/rates-bonds/france-20-year-bond-yield",
        "https://www.investing.com/rates-bonds/france-10-year-bond-yield",
        "https://www.investing.com/rates-bonds/france-5-year-bond-yield",
        "https://www.investing.com/rates-bonds/france-2-year-bond-yield",
        "https://www.investing.com/rates-bonds/france-1-year-bond-yield"
    ],

    "ITALY": [
        "https://www.investing.com/rates-bonds/italy-30-year-bond-yield",
        "https://www.investing.com/rates-bonds/italy-20-year-bond-yield",
        "https://www.investing.com/rates-bonds/italy-10-year-bond-yield",
        "https://www.investing.com/rates-bonds/italy-5-year-bond-yield",
        "https://www.investing.com/rates-bonds/italy-2-year-bond-yield",
        "https://www.investing.com/rates-bonds/italy-1-year-bond-yield"
    ],

    "UK": [
        "https://www.investing.com/rates-bonds/uk-30-year-bond-yield",
        "https://www.investing.com/rates-bonds/uk-20-year-bond-yield",
        "https://www.investing.com/rates-bonds/uk-10-year-bond-yield",
        "https://www.investing.com/rates-bonds/uk-5-year-bond-yield",
        "https://www.investing.com/rates-bonds/uk-2-year-bond-yield",
        "https://www.investing.com/rates-bonds/uk-1-year-bond-yield"
    ],

    "JAPAN": [
        "https://www.investing.com/rates-bonds/japan-30-year-bond-yield",
        "https://www.investing.com/rates-bonds/japan-20-year-bond-yield",
        "https://www.investing.com/rates-bonds/japan-10-year-bond-yield",
        "https://www.investing.com/rates-bonds/japan-5-year-bond-yield",
        "https://www.investing.com/rates-bonds/japan-2-year-bond-yield",
        "https://www.investing.com/rates-bonds/japan-1-year-bond-yield"
    ],

    "CANADA": [
        "https://www.investing.com/rates-bonds/canada-30-year-bond-yield",
        "https://www.investing.com/rates-bonds/canada-20-year-bond-yield",
        "https://www.investing.com/rates-bonds/canada-10-year-bond-yield",
        "https://www.investing.com/rates-bonds/canada-5-year-bond-yield",
        "https://www.investing.com/rates-bonds/canada-2-year-bond-yield",
        "https://www.investing.com/rates-bonds/canada-1-year-bond-yield"
    ],

    "BRAZIL": [
        "https://www.investing.com/rates-bonds/brazil-30-year-bond-yield",
        "https://www.investing.com/rates-bonds/brazil-20-year-bond-yield",
        "https://www.investing.com/rates-bonds/brazil-10-year-bond-yield",
        "https://www.investing.com/rates-bonds/brazil-5-year-bond-yield",
        "https://www.investing.com/rates-bonds/brazil-2-year-bond-yield",
        "https://www.investing.com/rates-bonds/brazil-1-year-bond-yield"
    ],

    "AUSTRALIA": [
        "https://www.investing.com/rates-bonds/australia-30-year-bond-yield",
        "https://www.investing.com/rates-bonds/australia-20-year-bond-yield",
        "https://www.investing.com/rates-bonds/australia-10-year-bond-yield",
        "https://www.investing.com/rates-bonds/australia-5-year-bond-yield",
        "https://www.investing.com/rates-bonds/australia-2-year-bond-yield",
        "https://www.investing.com/rates-bonds/australia-1-year-bond-yield"
    ]
}