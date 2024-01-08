import requests

# from src.TaxReturns.helpers.TOKENS import API_TOKEN

endpoint_url = "https://apitcstaging.pontte.com.br/TaxReturns/v1/"
def generate_pdf(pdf_payload, API_TOKEN):
    headers = {
        'Authorization': "Bearer " + API_TOKEN,
        'Content-Type': 'application/json'
    }

    # Bater no endpoint da torre de controle que gera o pdf
    response = requests.post(endpoint_url, headers=headers, json={'data': pdf_payload})

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to generate PDF: " + response.text)
