#!/usr/bin/python3

from flask import Flask, request, jsonify
import random
import datetime

app = Flask(__name__)

def generate_project_data(customer_name):
    project_names = [
        "Cloud Migration Initiative",
        "AI-Powered Analytics",
        "Security Compliance Enhancement",
        "Data Warehouse Modernization",
        "IoT Smart Operations"
    ]
    
    stakeholders = [
        "CTO", "CIO", "Cloud Architect", "Finance Director", "Product Manager"
    ]
    
    scopes = [
        "Optimizing Azure resources to enhance cost efficiency and performance.",
        "Implementing AI-driven insights to improve decision-making and automation.",
        "Ensuring regulatory compliance through advanced security protocols and monitoring.",
        "Modernizing data infrastructure to support scalability and real-time analytics.",
        "Leveraging IoT technologies for smart operations and predictive maintenance."
    ]
    
    project_name = random.choice(project_names)
    start_date = datetime.date.today() - datetime.timedelta(days=random.randint(30, 365))
    end_date = start_date + datetime.timedelta(days=random.randint(90, 365))
    acr_impact = round(random.uniform(10000, 500000), 2)
    scope = f"{customer_name} is undertaking the '{project_name}' project. {random.choice(scopes)} Success will be measured by adoption rates, cost reduction, and performance improvements."
    
    return {
        "customer_name": customer_name,
        "project_name": project_name,
        "start_date": start_date.strftime('%Y-%m-%d'),
        "estimated_end_date": end_date.strftime('%Y-%m-%d'),
        "estimated_acr_impact": acr_impact,
        "scope": scope,
        "main_stakeholders": random.sample(stakeholders, k=3)
    }

@app.route("/get_project_data", methods=["GET"])
def get_project_data():
    customer_name = request.args.get("customer_name")
    if not customer_name:
        return jsonify({"error": "Customer name is required"}), 400
    
    project_data = generate_project_data(customer_name)
    return jsonify(project_data)

if __name__ == "__main__":
    app.run(debug=True)

