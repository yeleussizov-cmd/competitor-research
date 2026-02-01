import requests
import csv
import time

# --- CONFIGURATION ---
API_KEY = 'AIzaSyCPCOFIcYCr7H6Z40IwrNKIrYii3pADUbM'
INPUT_FILE = 'companies.csv'
OUTPUT_FILE = 'company_place_ids.csv'

def get_place_id(query):
    """Fetches Place ID and address from Google Maps."""
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        'query': query,
        'key': API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if data.get('results'):
            # Grabbing the first (most relevant) result
            result = data['results'][0]
            return {
                'place_id': result.get('place_id'),
                'address': result.get('formatted_address'),
                'status': 'Success'
            }
        return {'place_id': '', 'address': '', 'status': 'No Result Found'}
    except Exception as e:
        return {'place_id': '', 'address': '', 'status': f'Error: {str(e)}'}

def run_bulk_lookup():
    print(f"Starting lookup for companies in {INPUT_FILE}...")
    
    results = []
    
    # Read the input file
    with open(INPUT_FILE, mode='r', encoding='utf-8') as f:
        # This handles both standard CSVs and simple text lists
        reader = csv.reader(f)
        company_names = [row[0] for row in reader if row]

    # Process each company
    for name in company_names:
        print(f"Searching for: {name}...")
        info = get_place_id(name)
        results.append({
            'company_query': name,
            'place_id': info['place_id'],
            'address': info['address'],
            'status': info['status']
        })
        # Optional: A tiny sleep to avoid hitting rate limits too fast
        time.sleep(0.1) 

    # Write to the output file
    keys = results[0].keys()
    with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nDone! Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    run_bulk_lookup()