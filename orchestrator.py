#!/usr/bin/python3

import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

def classify_query(query: str) -> str:
    """Classifies whether a query should go to devsquadagent or bingsearchagent."""
    dev_keywords = ["dev squad", "developer", "development", "software team"]
    if any(word in query.lower() for word in dev_keywords):
        return "devsquad"
    return "bingsearch"

# Initialize Azure AI Client
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(), conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)

def ask_agent(query: str, agent_id: str) -> str:
    """Sends a query to the specified agent."""
    try:
        thread = project_client.agents.create_thread()
        print(f"Created thread, ID: {thread.id}")
        
        project_client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content=query,
        )
        print("Message sent to agent.")
        
        run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent_id)
        print(f"Run status: {run.status}")
        
        if run.status == "failed":
            return f"Agent execution failed: {run.last_error}"
        
        messages = project_client.agents.list_messages(thread_id=thread.id)
        print(f"Retrieved {len(messages)} messages.")
        
        if not messages:
            return "No response received from the agent."
        
        last_message = messages[-1]
        if hasattr(last_message, "content"):
            return last_message.content
        else:
            return "Agent response format is unexpected."
    except Exception as e:
        return f"Error occurred while communicating with agent: {str(e)}"

def orchestrator(query: str) -> str:
    """Decides how to handle the query and routes it to the appropriate agent."""
    action = classify_query(query)
    agent_id = "asst_Rd75AJE67hMK2uqijmH9ez9D" if action == "devsquad" else "bingsearchagent"
    print(f"Routing query to: {agent_id}")
    return ask_agent(query, agent_id)

if __name__ == "__main__":
    user_query = input("Ask your question: ")
    response = orchestrator(user_query)
    print("Response:", response)

