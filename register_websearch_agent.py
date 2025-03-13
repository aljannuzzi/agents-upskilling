#!/usr/bin/python3

import requests

# Agent details
agent_data = {
    "agent_id": "asst_UvJQHfj4eap1uggLlLTMv4sn",
    "agent_name": "WebSearchAgent",
    "capabilities": ["internet search", "retrieving online data", "query classification", "I can query Bing for online information about any topic"]
}

# URL of the Agent Registry API
AGENT_REGISTRY_URL = "http://localhost:5000/register_agent"

# Register the agent
response = requests.post(AGENT_REGISTRY_URL, json=agent_data)

# Print the response
print(response.json())

