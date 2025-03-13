#!/usr/bin/python3

import requests

def get_project_data(customer_name):
    url = "http://127.0.0.1:5000/get_project_data"  # Update if deployed elsewhere
    params = {"customer_name": customer_name}
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Request failed with status code {response.status_code}"}

# Example usage
customer_name = "Bradesco"
project_data = get_project_data(customer_name)
print(project_data)

