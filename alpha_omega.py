import requests
import csv
import sys

# --- CONFIGURATION ---
API_KEY = "YOUR_API_KEY"
ORG_ID = "YOUR_ORG_ID" 
BASE_URL = "https://api.pulse.neat.no/v1" 

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def get_items(endpoint):
    """Fetches existing regions/locations from Neat Pulse"""
    url = f"{BASE_URL}/orgs/{ORG_ID}/{endpoint}"
    print(f"🔍 Fetching {endpoint}...")
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        return res.json().get('items', [])
    print(f"❌ Error fetching {endpoint}: {res.status_code}")
    return []

def setup_alpha(csv_file):
    print("\n🚀 ALPHA: Creating Hierarchy...")
    
    # Cache existing regions to prevent 409 Conflict errors
    existing_regs = {r['name']: r['id'] for r in get_items('regions')}
    
    with open(csv_file, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            reg_name = row['Region'].strip()
            loc_name = row['Location'].strip()

            # 1. Ensure Region exists
            if reg_name not in existing_regs:
                print(f" [+] Creating Region: {reg_name}")
                payload = {"name": reg_name}
                res = requests.post(f"{BASE_URL}/orgs/{ORG_ID}/regions", json=payload, headers=HEADERS)
                if res.status_code in [200, 201]:
                    existing_regs[reg_name] = res.json()['id']
            
            reg_id = existing_regs.get(reg_name)

            # 2. Create Location
            print(f" [+] Creating Location: {loc_name}")
            loc_payload = {
                "name": loc_name,
                "regionId": reg_id
            }
            requests.post(f"{BASE_URL}/orgs/{ORG_ID}/locations", json=loc_payload, headers=HEADERS)

    print("\n✨ Alpha Phase Complete.")

def nuke_omega():
    print("\n🧨 OMEGA: Wiping Environment...")
    
    # 1. Delete Locations first
    locations = get_items('locations')
    for loc in locations:
        print(f" [-] Deleting Location: {loc['name']}")
        requests.delete(f"{BASE_URL}/orgs/{ORG_ID}/locations/{loc['id']}", headers=HEADERS)
    
    # 2. Delete Regions
    regions = get_items('regions')
    for reg in regions:
        print(f" [-] Deleting Region: {reg['name']}")
        requests.delete(f"{BASE_URL}/orgs/{ORG_ID}/regions/{reg['id']}", headers=HEADERS)

    print("\n💨 Omega Phase Complete. Void returned.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python alpha_omega.py [setup|nuke]")
    elif sys.argv[1] == "setup":
        setup_alpha('deployment.csv')
    elif sys.argv[1] == "nuke":
        nuke_omega()