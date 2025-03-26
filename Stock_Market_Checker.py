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
sector = df["ISubgroup Name"].tolist()
industry = df["Industry New Name"].tolist()



stockInput = input("Enter Stock Name : ")
best_match,index = findBestMatch(stockInput,stock_names)
companyCode = code[index]


print(companyCode)
print(best_match)

sector_keywords = {
    "Software & IT Services": ["Tech", "digital economy", "tech news", "tech innovation", "tech growth", "technology trends", "tech disruption", "digital transformation", "tech giants", "tech startups", "venture capital", "cloud adoption", "AI development", "big data", "cybersecurity threats", "robotics advances", "internet speed", "automation impact", "data privacy", "tech regulation", "tech mergers", "industry partnerships", "supply chain", "hardware development", "tech policies"],
    "Finance": ["Finance", "financial crisis", "stock trends", "market volatility", "interest rates", "banking regulations", "credit risk", "investment strategies", "equity markets", "capital markets", "financial planning", "wealth management", "debt crisis", "market corrections", "financial growth", "financial stability", "funding rounds", "currency fluctuations", "risk management", "fiscal policies", "financial reports", "stock performance", "tax reforms", "global economy", "economic forecasting"],
    "Energy": ["Energy", "renewable growth", "oil price", "power consumption", "energy transition", "climate change", "green energy", "energy demand", "energy efficiency", "carbon emissions", "nuclear energy", "global warming", "power generation", "energy independence", "electric vehicles", "solar power", "wind power", "bioenergy", "hydropower", "energy investment", "sustainability goals", "energy security", "oil exploration", "natural gas", "energy policy", "electric grid"],
    "Healthcare": ["Healthcare", "medical research", "drug development", "health policy", "FDA approval", "health insurance", "patient care", "health access", "health equity", "medical advances", "disease prevention", "health systems", "clinical trials", "biotech innovation", "telemedicine growth", "pandemic response", "mental health", "medical costs", "public health", "health technology", "health legislation", "pharmaceutical research", "global health", "vaccination rates", "health disparities"],
    "Telecom": ["Telecom", "5G networks", "mobile services", "data traffic", "broadband access", "network upgrades", "wireless infrastructure", "spectrum allocation", "telecom mergers", "satellite internet", "IoT devices", "fiber optics", "telecom regulation", "network expansion", "mobile payments", "cellular technology", "network outages", "roaming charges", "tech giants", "telecom services", "communication platforms", "internet speed", "service providers", "data privacy", "telecom policy"],
     "Oil & Gas": ["Oil price", "natural gas", "crude oil", "energy supply", "oil exploration", "gas reserves", "drilling technology", "oil refinery", "pipeline construction", "global demand", "fuel prices", "hydraulic fracturing", "energy transition", "offshore drilling", "oil reserves", "gas production", "supply chain", "oil consumption", "refined products", "energy policy", "OPEC decisions", "oil exports", "energy security", "fossil fuels", "oil field", "gas transportation"]    
}

page_to_Scrape = requests.get(f"https://www.screener.in/company/{companyCode}",)
soup = BeautifulSoup(page_to_Scrape.text,"html.parser")

companyInfo = soup.find(class_="margin-0 show-from-tablet-landscape")
companyInfoList = companyInfo.text.split(" ")
print(companyInfo.text)
print()

# companyName = companyInfoList[1]

# companySecAndInd =companyInfoList[2]
# companySecAndIndList = companySecAndInd.split("|")

priceParent = soup.find(class_="flex flex-align-center")
currentPrice = priceParent.find('span')



if companyInfo:
    print("Company Name : " + best_match)
    print("Sector : " + sector[index])
    print("Industry : " + industry[index])
    print("\n")
    print("Current Price : " + currentPrice.text)
else:
    print("Company not found")

# if sector[index] in sector_keywords:
#     keywords = sector_keywords[companySector]
# else:print("no")

