#!/usr/bin/python3

import requests

# URL of the Agent Registry API
AGENT_REGISTRY_URL = "http://localhost:5000/list_agents"

def list_capabilities():
    """Fetches and displays all registered agent capabilities."""
    response = requests.get(AGENT_REGISTRY_URL)
    
    if response.status_code == 200:
        agents = response.json()
        for agent_id, details in agents.items():
            print(f"Agent ID: {agent_id}")
            print(f"Agent Name: {details['agent_name']}")
            print(f"Capabilities: {', '.join(details['capabilities'])}")
            print(f"Registered At: {details['registered_at']}")
            print("-" * 40)
    else:
        print(f"Error: Failed to fetch agents (Status Code: {response.status_code})")

if __name__ == "__main__":
    list_capabilities()

