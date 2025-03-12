#!/usr/bin/python3

import os
import logging
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
        # Create a new thread
        thread = project_client.agents.create_thread()
        logger.debug(f"Created thread, ID: {thread.id}")

        # Send the user's query as a message
        project_client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content=query,
        )
        logger.debug("Message sent to agent.")

        # Process the run
        run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent_id)
        logger.debug(f"Run status: {run.status}")

        if run.status == "failed":
            logger.error(f"Run failed with error: {run.last_error}")
            return f"Agent execution failed: {run.last_error}"

        # Retrieve messages from the agent
        messages = project_client.agents.list_messages(thread_id=thread.id)
        logger.debug(f"Retrieved {len(messages)} messages.")

        if not messages:
            return "No response received from the agent."

        # Process each message
        for idx, message in enumerate(messages):
            logger.debug(f"Message {idx}: {message}")
            if hasattr(message, "content"):
                content = message.content
                logger.debug(f"Content: {content}")
                if isinstance(content, str):
                    return content
                elif isinstance(content, dict):
                    # Attempt to extract 'data' from the response
                    data = content.get('data', 'No data found')
                    return f"Agent response data: {data}"
                else:
                    logger.error(f"Unexpected content type: {type(content)}")
                    return f"Unexpected content format: {type(content)}"
            else:
                logger.error("No content attribute found in message.")
                return "Agent response format is unexpected."

    except Exception as e:
        logger.exception("Exception occurred while communicating with agent")
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

