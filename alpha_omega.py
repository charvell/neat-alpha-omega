import requests
import csv
import sys

# --- Configuration ---
# Pro-tip: Keep these in a config.py file ignored by git!
try:
    import config
    API_KEY = config.API_KEY
    ORG_ID = config.ORG_ID
except ImportError:
    API_KEY = "YOUR_KEY"
    ORG_ID = "YOUR_ID"

BASE_URL = f"https://api.pulse.neat.no/v1/orgs/{ORG_ID}"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def show_banner(mode):
    banner = f"""
    ##########################################
    #          NEAT: ALPHA & OMEGA           #
    #        Mode: {mode.upper():<25} #
    ##########################################
    """
    print(banner)

def setup_from_csv(file_path):
    show_banner("Alpha (Creation)")
    # ... (rest of your setup logic)
    print("\n✨ Deployment Complete. The environment is live.")

def nuke_all():
    show_banner("Omega (Teardown)")
    # ... (rest of your nuke logic)
    print("\n💨 The environment has been returned to void.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python alpha_omega.py [setup|nuke]")
    elif sys.argv[1] == "setup":
        setup_from_csv('deployment.csv')
    elif sys.argv[1] == "nuke":
        nuke_all()