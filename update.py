import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from zoneinfo import ZoneInfo

ACCOUNT_ID = os.environ["ROBO_ACCOUNT_ID"]
API_KEY = os.environ["ROBO_API_KEY"]

URL = f"https://my.roboforex.com/api/partners/tree?account_id={ACCOUNT_ID}&api_key={API_KEY}"

print("Downloading XML...")

response = requests.get(URL, timeout=30)

print("HTTP Status:", response.status_code)

if response.status_code != 200:
    raise Exception(f"HTTP Error {response.status_code}")

xml = response.text.strip()

if not xml.startswith("<"):
    print(xml)
    raise Exception("RoboForex did not return XML.")

root = ET.fromstring(xml)

# Collect ALL account IDs recursively
accounts = []

for acc in root.iter("account"):
    if "id" in acc.attrib:
        accounts.append(acc.attrib["id"])

# Remove duplicates while preserving order
accounts = list(dict.fromkeys(accounts))

print(f"Found {len(accounts)} accounts")

# Thailand time (12-hour format)
timestamp = datetime.now(
    ZoneInfo("Asia/Bangkok")
).strftime("%Y-%m-%d %I:%M:%S %p")

FILE = "ManusNexus.txt"

with open(FILE, "r", encoding="utf-8") as f:
    text = f.read()

marker = "Auto Update Roboforex Clients:"

if marker not in text:
    raise Exception("Cannot find 'Auto Update Roboforex Clients:' in ManusNexus.txt")

before = text.split(marker)[0]

new_text = before
new_text += marker + "\n\n"
new_text += f"# Last updated: {timestamp}\n"

for acc in accounts:
    new_text += acc + "\n"

with open(FILE, "w", encoding="utf-8") as f:
    f.write(new_text)

print("Done.")
