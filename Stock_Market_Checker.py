from bs4 import BeautifulSoup
import requests
from thefuzz import fuzz,process
import pandas as pd

df = pd.read_csv(r"D:\Mishal\Projects - College\External Study\Stock Market Watcher\stock-watcher\stock_names.csv")

def findBestMatch(query, choices, threshold=80):
    match = process.extractOne(query, choices, score_cutoff=threshold)
    index = choices.index(match[0])
    return match[0],index if match else None

stock_names = df["Issuer Name"].tolist()
code = df["Security Code"].tolist()
industry = df["Industry New Name"].tolist()



stockInput = input("Enter Stock Name : ")
best_match,index = findBestMatch(stockInput,stock_names)
companyCode = code[index]

stock_news_keywords = {
    "Aerospace & Defence": ["contracts", "military spending", "exports", "geopolitical tensions", "government deals", "R&D funding"],
    "Agro Chemicals": ["crop yield", "monsoon", "fertilizer subsidy", "pesticide ban", "commodity prices", "regulations"],
    "Air Transport Service": ["fuel prices", "passenger traffic", "airline mergers", "regulations", "air traffic control", "strike"],
    "Alcoholic Beverages": ["excise duty", "sales ban", "new product launch", "liquor policy", "consumer demand"],
    "Auto Ancillaries": ["EV demand", "chip shortage", "supply chain", "export growth", "R&D investment"],
    "Automobile": ["EV adoption", "fuel prices", "auto sales", "emission norms", "government incentives"],
    "Banks": ["interest rates", "loan defaults", "credit growth", "regulatory policy", "NPAs", "mergers"],
    "Bearings": ["manufacturing growth", "auto sector demand", "global trade", "industrial expansion"],
    "Cables": ["infrastructure investment", "fiber optic expansion", "copper prices", "electric vehicle wiring"],
    "Capital Goods - Electrical Equipment": ["power demand", "renewable energy", "infrastructure projects", "government contracts"],
    "Capital Goods-Non Electrical Equipment": ["industrial production", "construction demand", "manufacturing index", "export orders"],
    "Castings, Forgings & Fasteners": ["auto sector growth", "defense contracts", "manufacturing expansion", "raw material costs"],
    "Cement": ["real estate growth", "construction demand", "government projects", "coal prices"],
    "Cement - Products": ["infrastructure spending", "urbanization", "real estate sector", "cost of raw materials"],
    "Ceramic Products": ["housing demand", "export growth", "decor trends", "government policies"],
    "Chemicals": ["export restrictions", "input costs", "R&D developments", "industrial demand"],
    "Computer Education": ["digital transformation", "IT job growth", "government training programs"],
    "Construction": ["infrastructure projects", "housing sector", "government spending", "raw material prices"],
    "Consumer Durables": ["festive season sales", "disposable income", "import tariffs", "new product launches"],
    "Credit Rating Agencies": ["interest rate changes", "debt defaults", "economic outlook", "corporate credit"],
    "Crude Oil & Natural Gas": ["OPEC decisions", "supply chain", "exploration projects", "fuel price hikes"],
    "Diamond, Gems and Jewellery": ["gold prices", "export demand", "festive season", "government import policy"],
    "Diversified": ["macro economy", "investment trends", "company restructuring"],
    "Dry cells": ["battery technology", "raw material costs", "demand from EV sector"],
    "E-Commerce/App based Aggregator": ["consumer spending", "regulatory policies", "discount wars", "logistics cost"],
    "Edible Oil": ["commodity prices", "import duties", "crop yield", "global supply chain"],
    "Education": ["government policies", "digital learning", "new education initiatives"],
    "Electronics": ["semiconductor supply", "import duties", "consumer demand", "innovation"],
    "Engineering": ["infrastructure growth", "R&D investment", "export orders"],
    "Entertainment": ["OTT growth", "advertising revenue", "regulatory changes", "consumer trends"],
    "ETF": ["market volatility", "inflation", "monetary policy", "sector rotation"],
    "Ferro Alloys": ["steel demand", "import-export rules", "raw material prices"],
    "Fertilizers": ["crop yield", "government subsidies", "weather conditions", "global trade"],
    "Finance": ["interest rates", "loan growth", "mergers & acquisitions"],
    "Financial Services": ["regulatory policies", "fintech adoption", "credit growth"],
    "FMCG": ["consumer spending", "raw material costs", "brand expansion"],
    "Gas Distribution": ["natural gas prices", "urban expansion", "government subsidies"],
    "Glass & Glass Products": ["real estate sector", "construction demand", "exports"],
    "Healthcare": ["drug approvals", "pandemic impact", "government policies"],
    "Hotels & Restaurants": ["tourism growth", "festive season", "regulatory changes"],
    "Infrastructure Developers & Operators": ["government projects", "PPP investments", "foreign direct investment"],
    "Infrastructure Investment Trusts": ["real estate demand", "dividends", "interest rates"],
    "Insurance": ["policyholder trends", "new regulations", "market competition"],
    "IT - Hardware": ["chip shortages", "government policies", "innovation"],
    "IT - Software": ["outsourcing demand", "cybersecurity issues", "AI adoption"],
    "Leather": ["export demand", "fashion trends", "raw material costs"],
    "Logistics": ["fuel costs", "e-commerce growth", "supply chain issues"],
    "Marine Port & Services": ["import-export trade", "infrastructure projects", "fuel prices"],
    "Media - Print/Television/Radio": ["advertising revenue", "subscription growth", "digital transformation"],
    "Mining & Mineral products": ["commodity prices", "government policies", "demand from industries"],
    "Miscellaneous": ["economic trends", "regulatory updates", "market disruptions"],
    "Non Ferrous Metals": ["global trade", "industrial demand", "price fluctuations"],
    "Oil Drill/Allied": ["crude oil prices", "exploration projects", "government regulations"],
    "Online Media": ["advertising trends", "subscription growth", "content regulations"],
    "Packaging": ["e-commerce growth", "recycling policies", "raw material costs"],
    "Paints/Varnish": ["housing demand", "raw material costs", "brand expansion"],
    "Paper": ["digital substitution", "import tariffs", "demand from packaging"],
    "Petrochemicals": ["oil prices", "chemical demand", "regulatory changes"],
    "Pharmaceuticals": ["drug approvals", "R&D investment", "global health trends"],
    "Plantation & Plantation Products": ["crop yield", "climate change", "export policies"],
    "Plastic products": ["recycling regulations", "raw material costs", "manufacturing demand"],
    "Plywood Boards/Laminates": ["construction growth", "housing trends", "import costs"],
    "Power Generation & Distribution": ["renewable energy", "government subsidies", "electricity demand"],
    "Power Infrastructure": ["grid expansion", "investment policies", "government projects"],
    "Printing & Stationery": ["digital transformation", "education demand", "import costs"],
    "Quick Service Restaurant": ["consumer spending", "franchise growth", "food inflation"],
    "Railways": ["government investments", "infrastructure projects", "ticket pricing"],
    "Readymade Garments/ Apparels": ["fashion trends", "export demand", "raw material costs"],
    "Real Estate Investment Trusts": ["property market trends", "interest rates", "urbanization"],
    "Realty": ["housing demand", "construction cost", "government subsidies"],
    "Refineries": ["oil prices", "government regulations", "capacity expansion"],
    "Refractories": ["industrial demand", "construction growth", "raw material costs"],
    "Retail": ["festive season sales", "consumer sentiment", "e-commerce competition"],
    "Sanitaryware": ["housing trends", "real estate demand", "import tariffs"],
    "Ship Building": ["defense contracts", "global trade", "raw material costs"],
    "Shipping": ["freight rates", "fuel prices", "global trade"],
    "Steel": ["demand from auto & construction", "global steel prices", "export tariffs"],
    "Stock/Commodity Brokers": ["market volatility", "trading volumes", "interest rates"],
    "Sugar": ["commodity prices", "government subsidies", "climate impact"],
    "Telecom-Handsets/Mobile": ["5G adoption", "import tariffs", "chip shortages"],
    "Telecomm Equipment & Infra Services": ["5G rollout", "government policies", "infrastructure investment"],
    "Telecomm-Service": ["ARPU growth", "subscriber base", "government regulations"],
    "Textiles": ["export demand", "raw material costs", "fashion trends"],
    "Tobacco Products": ["excise duty", "smoking regulations", "consumer demand"],
    "Trading": ["market trends", "import-export rules", "economic growth"],
    "Tyres": ["raw material costs", "auto sector demand", "export growth"]
}



company_to_Scrape = requests.get(f"https://www.screener.in/company/{companyCode}",)
soup = BeautifulSoup(company_to_Scrape.text,"html.parser")

companyInfo = soup.find(class_="margin-0 show-from-tablet-landscape")
companyInfoList = companyInfo.text.split(" ")
print(companyInfo.text)
print()



priceParent = soup.find(class_="flex flex-align-center")
currentPrice = priceParent.find('span')

sectorParent = soup.find(id="peers")
sectorName = sectorParent.find('a').text

if companyInfo:
    print("Company Name : " + best_match)
    print("Sector : " + sectorName)
    print("Industry : " + industry[index])
    print("\n")
    print("Current Price : " + currentPrice.text)
else:
    print("Company not found")


news_to_Scrape = requests.get(f"https://news.google.com/search?q=India-{sectorName} when:1d")
newsHeaders = soup.findAll("a",class_="JtKRv")
for i in newsHeaders:
    print(i.text)


