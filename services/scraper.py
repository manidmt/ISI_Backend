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


from models.bond import Bond, Session
from datetime import datetime

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

        # Último valor (yield)
        yield_tag = soup.find('span', class_='text-5xl/8 font-bold')
        yield_pct = float(yield_tag.text.strip().replace('%', '')) if yield_tag else None

        # Cambio absoluto y porcentaje
        change_container = soup.find('div', class_='flex items-end gap-1')
        if change_container:
            spans = change_container.find_all('span')
            if len(spans) >= 2:
                daily_change = float(spans[0].text.strip().replace('+', '').replace(',', ''))
                daily_change_pct = float(spans[1].text.strip().replace('(', '').replace(')', '').replace('%', '').replace('+', '').replace(',', ''))
            else:
                daily_change = None
                daily_change_pct = None
        else:
            daily_change = None
            daily_change_pct = None

        # Última actualización
        update_tag = soup.find('span', class_='text-xs text-secondary-text')
        if update_tag:
            update_text = update_tag.text.strip()
            try:
                last_update = datetime.strptime(update_text, "%b %d, %Y %H:%M UTC")
            except Exception:
                last_update = None
        else:
            last_update = None

        # Moneda (currency) de forma correcta
        currency_tag = soup.find('div', attrs={"data-test": "currency-in-label"})
        if currency_tag:
            span_currency = currency_tag.find('span')
            currency = span_currency.text.strip() if span_currency else "Currency no encontrada"
        else:
            currency = "Currency no encontrada"

        # Guardarlo en base de datos
        session = Session()
        new_bond = Bond(
            country=country,
            name=name,
            yield_pct=yield_pct,
            daily_change=daily_change,
            daily_change_pct=daily_change_pct,
            last_update=last_update,
            currency=currency
        )
        session.add(new_bond)
        session.commit()
        session.close()

        return {
            "country": country,
            "name": name,
            "yield_pct": yield_pct,
            "daily_change": daily_change,
            "daily_change_pct": daily_change_pct,
            "last_update": last_update,
            "currency": currency
        }

    except Exception as e:
        return {"error": f"Error extrayendo datos: {str(e)}"}


def scrape_or_get_bond_info(url, country):
    today = datetime.today().date()

    # Scrapeamos para conocer el nombre exacto del bono
    scraped_data = scrape_bond_info(url, country)
    name = scraped_data.get("name")

    if not name:
        return {"error": "No se pudo extraer el nombre del bono"}

    session = Session()
    existing = session.query(Bond).filter_by(name=name, country=country).first()

    # Si ya existe y está actualizado, lo devolvemos
    if existing and existing.last_update and existing.last_update.date() == today:
        session.close()
        return {
            "id": existing.id,
            "country": existing.country,
            "name": existing.name,
            "yield_pct": existing.yield_pct,
            "daily_change": existing.daily_change,
            "daily_change_pct": existing.daily_change_pct,
            "last_update": existing.last_update,
            "currency": existing.currency
        }

    session.close()
    # Si no existe o está desactualizado, devolvemos el scrapeo (que ya viene de bond_scraper.py y guarda en DB)
    return scraped_data

def get_bonds_info(country):
    country = country.upper()
    urls = bonds_urls.get(country)
    if not urls:
        return {"error": "País no soportado"}

    bond_data = []
    for url in urls:
        data = scrape_or_get_bond_info(url, country)
#        if "error" in data:
#            return data
        bond_data.append(data)

    return bond_data