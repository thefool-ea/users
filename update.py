
import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from zoneinfo import ZoneInfo

ACCOUNT_ID = os.environ["ROBO_ACCOUNT_ID"]
API_KEY = os.environ["ROBO_API_KEY"]

URL = f"https://my.roboforex.com/api/partners/tree?account_id={ACCOUNT_ID}&api_key={API_KEY}"

# Download XML
xml = requests.get(URL, timeout=30).text
root = ET.fromstring(xml)

# Collect account IDs
accounts = []
accounts.append(ACCOUNT_ID)  # include your own account
for acc in root.findall(".//referrals/account"):
    accounts.append(acc.attrib["id"])

# Thailand time (12-hour format)
timestamp = datetime.now(
    ZoneInfo("Asia/Bangkok")
).strftime("%Y-%m-%d %I:%M:%S %p")

# Read existing file
FILE = "ManusNexus.txt"

with open(FILE, "r", encoding="utf-8") as f:
    text = f.read()

marker = "Auto Update Roboforex Clients:"

if marker not in text:
    raise Exception("Cannot find 'Auto Update Roboforex Clients:' in ManusNexus.txt")

# Keep everything before the marker
before = text.split(marker)[0]

# Build new auto section
new_section = marker + "\n\n"
new_section += f"# Last updated: {timestamp}\n"

for acc in accounts:
    new_section += acc + "\n"

# Write file
with open(FILE, "w", encoding="utf-8") as f:
    f.write(before + new_section)

print("Updated successfully.")
