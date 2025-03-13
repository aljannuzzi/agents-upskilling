#!/usr/bin/python3

import requests

# Agent details
agent_data = {
    "agent_id": "asst_Rd75AJE67hMK2uqijmH9ez9D",
    "agent_name": "DevSquadAgent",
    "capabilities": ["software development", "team management", "code review", "I can talk about projects executed by the Dev Squad team to provide insights about projec goals, architecture definition and the development challenges"]
}

# URL of the Agent Registry API
AGENT_REGISTRY_URL = "http://localhost:5000/register_agent"

# Register the agent
response = requests.post(AGENT_REGISTRY_URL, json=agent_data)

# Print the response
print(response.json())
