import requests
from bs4 import BeautifulSoup
from models.company import Company, Session
from models.bond import bonds_urls

def scrape_or_get_company_info(symbol):
    session = Session()

    # 1. Buscar primero en la base de datos
    company = session.query(Company).filter_by(symbol=symbol).first()
    if company:
        session.close()
        return {
            "symbol": company.symbol,
            "name": company.name,
            "sector": company.sector,
            "industry": company.industry
        }

    # 2. Si no existe, scrapear
    url = f"https://finance.yahoo.com/quote/{symbol}/profile"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        session.close()
        return {"error": f"Error {response.status_code} al acceder a Yahoo Finance"}

    soup = BeautifulSoup(response.text, "html.parser")

    try:
        # Extraer nombre
        name_tag = soup.find('title')
        if name_tag:
            name_full = name_tag.text.strip()
            name = name_full.split('(')[0].strip()
        else:
            name = "Nombre no encontrado"

        # Extraer sector e industria
        sector = "Sector no encontrado"
        industry = "Industria no encontrada"

        dt_tags = soup.find_all('dt', class_='yf-wxp4ja')

        for dt in dt_tags:
            text = dt.text.strip()
            if text == "Sector:":
                dd = dt.find_next_sibling('dd')
                if dd:
                    sector = dd.text.strip()
            elif text == "Industry:":
                a = dt.find_next_sibling('a')
                if a:
                    industry = a.text.strip()

        # 3. Guardar en la base de datos
        new_company = Company(
            symbol=symbol,
            name=name,
            sector=sector,
            industry=industry
        )
        session.add(new_company)
        session.commit()

        session.close()

        return {
            "symbol": symbol,
            "name": name,
            "sector": sector,
            "industry": industry
        }

    except Exception as e:
        session.close()
        return {"error": f"Error extrayendo datos: {str(e)}"}



import requests
from bs4 import BeautifulSoup
from datetime import datetime
from models.bond import Bond, Session, extract_bond_name_from_url
import time

def scrape_bond_info(url, country):
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"error": f"Error {response.status_code} al acceder a Investing.com"}

    soup = BeautifulSoup(response.text, "html.parser")

    try:
        # Nombre del bono
        title_tag = soup.find('h1')
        name = title_tag.text.strip() if title_tag else "Nombre no encontrado"
        print(f"Nombre del bono: {name}")
        # Inicializar variables
        currency = "Currency no encontrada"
        prev_close = None
        day_range = None
        year_range = None
        price = None
        price_range = None
        coupon = None
        maturity_date = None
        one_year_change = None

        # Buscar los datos del bloque de "Key Info"
        key_info = soup.find('div', attrs={"data-test": "key-info"})
        if key_info:
            rows = key_info.find_all('div', class_='flex flex-wrap items-center justify-between border-t border-t-[#e6e9eb] pt-2.5 sm:pb-2.5 pb-2.5')
            for row in rows:
                label_tag = row.find('dt')
                value_tag = row.find('dd')
                if not label_tag or not value_tag:
                    continue
                label = label_tag.text.strip()
                value = value_tag.text.strip()


                if label in ["Price", "Price Range", "1-Year Change"]:
                    spans = value_tag.find_all('span')

                    if label == "Price":
                        # Sacar el primer número
                        nums = [span.text.strip() for span in spans if span.text.strip() and span.text.strip() != '-']
                        if nums:
                            try:
                                price = float(nums[0].replace(',', ''))
                            except:
                                price = None

                    elif label == "Price Range":
                        nums = [span.text.strip() for span in spans if span.text.strip() and span.text.strip() != '-']
                        if len(nums) >= 2:
                            price_range = f"{nums[0]}-{nums[1]}"
                        else:
                            price_range = "-"

                    elif label == "1-Year Change":
                        # Buscamos directamente en value_tag el texto combinado
                        main_span = value_tag.find('span', class_='key-info_dd-numeric__ZQFIs')
                        if main_span:
                            child_spans = main_span.find_all('span')
                            if len(child_spans) >= 2:
                                try:
                                    number_text = child_spans[1].text.strip()  # El número está en el segundo span
                                    one_year_change = float(number_text.replace(',', ''))
                                except:
                                    one_year_change = None


                if label == "Prev. Close":
                    prev_close = float(value) if value else None
                elif label == "Day's Range":
                    day_range = value
                elif label == "52 wk Range":
                    year_range = value
                #elif label == "Price":
                #    price = float(value) if value and value != "-" else None
                #elif label == "Price Range":
                #    price_range = value
                elif label == "Coupon":
                    coupon = float(value) if value and value != "-" else None
                elif label == "Maturity Date":
                    maturity_date = value
                #elif label == "1-Year Change":
                #    one_year_change = float(value.replace('%', '').replace(',', '')) if value else None

        # Moneda (currency)
        currency_tag = soup.find('div', attrs={"data-test": "currency-in-label"})
        if currency_tag:
            span_currency = currency_tag.find('span')
            currency = span_currency.text.strip() if span_currency else "Currency no encontrada"

        print(f"Datos del bono: {name}")
        print(f"  - Currency: {currency}")
        print(f"  - Prev. Close: {prev_close}")
        print(f"  - Day's Range: {day_range}")
        print(f"  - 52 wk Range: {year_range}")
        print(f"  - Price: {price}")
        print(f"  - Price Range: {price_range}")
        print(f"  - Coupon: {coupon}")
        print(f"  - Maturity Date: {maturity_date}")
        print(f"  - 1-Year Change: {one_year_change}")

        return {
            "country": country,
            "name": name,
            "currency": currency,
            "prev_close": prev_close,
            "day_range": day_range,
            "year_range": year_range,
            "price": price,
            "price_range": price_range,
            "coupon": coupon,
            "maturity_date": maturity_date,
            "one_year_change": one_year_change
        }

    except Exception as e:
        return {"error": f"Error extrayendo datos: {str(e)}"}

def scrape_or_get_bond_info(url, country):
    today = datetime.today().date()

    # Scrapeamos para conocer el nombre exacto del bono
    name = extract_bond_name_from_url(url)
    if not name:
        return {"error": "No se pudo extraer el nombre del bono"}

    session = Session()
    existing = session.query(Bond).filter_by(name=name, country=country).first()

    # Si ya existe y está actualizado, lo devolvemos
    if existing and existing.last_update and existing.last_update.date() == today:
        session.close()
        return {
            "country": existing.country,
            "name": existing.name,
            "currency": existing.currency,
            "prev_close": existing.prev_close,
            "day_range": existing.day_range,
            "year_range": existing.year_range,
            "price": existing.price,
            "price_range": existing.price_range,
            "coupon": existing.coupon,
            "maturity_date": existing.maturity_date,
            "one_year_change": existing.one_year_change
        }

    scraped_data = scrape_bond_info(url, country)
    new_bond = Bond(
        country=country,
        name=scraped_data["name"],
        currency=scraped_data["currency"],
        prev_close=scraped_data["prev_close"],
        day_range=scraped_data["day_range"],
        year_range=scraped_data["year_range"],
        price=scraped_data["price"],
        price_range=scraped_data["price_range"],
        coupon=scraped_data["coupon"],
        maturity_date=scraped_data["maturity_date"],
        one_year_change=scraped_data["one_year_change"],
        last_update=datetime.now()
    )
    session.add(new_bond)
    session.commit()
    session.close()
    time.sleep(5)
    # Si no existe o está desactualizado, devolvemos el scrapeo (que ya viene de bond_scraper.py y guarda en DB)
    return scraped_data

def get_bonds_info(country):
    country = country.upper()
    urls = bonds_urls.get(country)
    if not urls:
        return {"error": "País no soportado"}
    
    bonds_data = []
    for url in urls:
        data = scrape_or_get_bond_info(url, country)
        if "error" not in data:
            bonds_data.append(data)

    return bonds_data


