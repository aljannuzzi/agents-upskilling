#!/usr/bin/python3

import os
import requests
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import MessageTextContent
from azure.identity import DefaultAzureCredential

# Agent Registry API URL (update with your actual deployed URL)
AGENT_REGISTRY_URL = "http://localhost:5000/list_agents"

# AI Foundry Classifier Agent ID (Replace with your actual agent ID)
CLASSIFIER_AGENT_ID = "asst_d06PXAZyEccq4BwOXbt34jpj"

# Initialize Azure AI Client
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(), conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)

def get_registered_agents():
    """Fetches registered agents and their capabilities from the Agent Registry API."""
    response = requests.get(AGENT_REGISTRY_URL)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching agents: {response.status_code}")
        return {}

def ask_classifier_agent(query: str, agents_data: dict) -> str:
    """Asks the AI Foundry classifier agent which agent is best suited for the query."""
    try:
        # Create a new thread
        thread = project_client.agents.create_thread()
        print(f"Created thread, ID: {thread.id}")

        # Send the classification request to the agent
        agents_list = ", ".join([f"{aid}: {data['capabilities']}" for aid, data in agents_data.items()])
        classification_prompt = (
            f"Based on the following registered agents and their capabilities:\n{agents_list}\n\n"
            f"Which agent should handle this query: '{query}'? Return only the agent ID."
        )

        project_client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content=classification_prompt,
        )
        print("Classification request sent to AI Foundry classifier agent.")

        # Process the agent's response
        run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=CLASSIFIER_AGENT_ID)
        print(f"Run status: {run.status}")

        if run.status == "failed":
            return None

        # Retrieve response from classifier agent
        messages = project_client.agents.list_messages(thread_id=thread.id)
        if not messages.data:
            return None

        for message in reversed(messages.data):
            if message.role == "assistant" and isinstance(message.content, list):
                for content_item in message.content:
                    if isinstance(content_item, MessageTextContent):
                        return content_item.text.value.strip()

    except Exception as e:
        print(f"Error occurred while querying classifier agent: {str(e)}")
    
    return None

def ask_agent(query: str, agent_id: str) -> str:
    """Sends a query to the selected agent and retrieves the response."""
    try:
        # Create a new thread
        thread = project_client.agents.create_thread()
        print(f"Created thread, ID: {thread.id}")

        # Send the user's message to the agent
        project_client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content=query,
        )
        print("Message sent to agent.")

        # Process the agent's response
        run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent_id)
        print(f"Run status: {run.status}")

        if run.status == "failed":
            return f"Agent execution failed: {run.last_error}"

        # Retrieve all messages in the thread
        messages = project_client.agents.list_messages(thread_id=thread.id)
        if not messages.data:
            return "No response received from the agent."

        # Extract assistant's response
        for message in reversed(messages.data):
            if message.role == "assistant" and isinstance(message.content, list):
                for content_item in message.content:
                    if isinstance(content_item, MessageTextContent):
                        return content_item.text.value

        return "Agent response format is unexpected."

    except Exception as e:
        return f"Error occurred while communicating with agent: {str(e)}"

def orchestrator(query: str) -> str:
    """Fetches registered agents, asks AI Foundry classifier which agent to use, and routes query."""
    agents_data = get_registered_agents()
    
    if not agents_data:
        return "No agents are registered."

    agent_id = ask_classifier_agent(query, agents_data)

    if not agent_id or agent_id not in agents_data:
        return "No suitable agent found for this query."

    print(f"Routing query to agent: {agent_id}")
    return ask_agent(query, agent_id)

if __name__ == "__main__":
    user_query = input("Ask your question: ")
    response = orchestrator(user_query)
    print("Response:", response)

