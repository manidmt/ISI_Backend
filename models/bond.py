from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Bond(Base):
    __tablename__ = 'bonds'

    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String)         
    name = Column(String)          
    prev_close = Column(Float)
    day_range = Column(String) 
    year_range = Column(String) 
    price = Column(Float)
    price_range = Column(String)  
    coupon = Column(Float)  
    maturity_date = Column(String)
    one_year_change = Column(Float)   
    currency = Column(String)      
    last_update = Column(DateTime)

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





import re
def extract_bond_name_from_url(url):
    try:
        # 1. Cogemos solo la parte después de '/rates-bonds/'
        path = url.split('/rates-bonds/')[-1]

        # 2. Quitamos '-bond-yield' al final
        path = path.replace('-bond-yield', '')

        # 3. Separamos por guiones
        parts = path.split('-')

        # 4. El país puede tener varios guiones (ej: south-korea), unimos todo excepto los dos últimos
        if len(parts) >= 2:
            country_parts = parts[:-2]  # Todo menos los dos últimos
            years_number = parts[-2]    # Por ejemplo "10"
            year_word = parts[-1]        # "year"

            # Formar país
            country = ' '.join([p.capitalize() for p in country_parts])

            # Asegurar que "Year" tenga Y mayúscula
            year_part = f"{years_number}-Year"

            name = f"{country} {year_part} Bond Yield"
        else:
            name = path.replace('-', ' ').title()

        return name

    except Exception as e:
        print(f"Error extrayendo nombre del bono: {str(e)}")
        return None


# Ejemplo de uso:
url1 = "https://www.investing.com/rates-bonds/spain-10-year-bond-yield"
url2 = "https://www.investing.com/rates-bonds/germany-20-year-bond-yield"
url3 = "https://www.investing.com/rates-bonds/france-5-year-bond-yield"

print(extract_bond_name_from_url(url1))
print(extract_bond_name_from_url(url2))
print(extract_bond_name_from_url(url3))