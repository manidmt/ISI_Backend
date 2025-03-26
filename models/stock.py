from sqlalchemy import Column, String, Float, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Stock(Base):
    __tablename__ = 'stocks'
    
    symbol = Column(String, primary_key=True)
    date = Column(Date, primary_key=True)
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Float)
    variation_pct = Column(Float)

# Configurar conexión a SQLite
engine = create_engine('sqlite:///stocks.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
