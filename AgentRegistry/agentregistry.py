#!/usr/bin/python3

from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

# In-memory storage for agent capabilities
registered_agents = {}

@app.route("/register_agent", methods=["POST"])
def register_agent():
    """Registers an agent's capabilities with a provided ID."""
    data = request.json

    if not data or "agent_id" not in data or "agent_name" not in data or "capabilities" not in data:
        return jsonify({"error": "Missing required fields: agent_id, agent_name, capabilities"}), 400

    agent_id = data["agent_id"]
    agent_name = data["agent_name"]
    capabilities = data["capabilities"]

    # Store the agent capabilities
    registered_agents[agent_id] = {
        "agent_name": agent_name,
        "capabilities": capabilities,
        "registered_at": datetime.datetime.utcnow().isoformat()
    }

    return jsonify({"message": f"Agent '{agent_name}' registered successfully", "agent_id": agent_id}), 201

@app.route("/list_agents", methods=["GET"])
def list_agents():
    """Returns a list of registered agents with their IDs and capabilities."""
    return jsonify(registered_agents)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

