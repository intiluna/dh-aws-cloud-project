import sys
import requests
import csv

def upload_records_to_endpoint(endpoint_url):
    # Read records from CSV file
    endpoint_url = endpoint_url + '/anuncios'
    print(endpoint_url)
    with open('records_to_populate_db.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Extract userId and name from CSV row
            anuncioId = row['anuncioId']
            titulo = row['titulo']
            precio = row['precio']
            email = row['email']
            print(f"anuncio_id:_{anuncioId}, titulo:_{titulo}")
            # Make POST request to upload record

            response = requests.post(endpoint_url, json={"anuncioId": anuncioId, "titulo": titulo,"precio": precio,"email": email})
            
            # Print response
            print(response.json())

if __name__ == "__main__":
    # Check if the endpoint URL is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python preload_using_endpoint.py <endpoint_url>")
        sys.exit(1)
    
    endpoint_url = sys.argv[1]
    upload_records_to_endpoint(endpoint_url)
