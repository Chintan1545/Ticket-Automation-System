import pandas as pd
import re
from datetime import datetime, timedelta
import uuid
import os

# Routing rules
ROUTING_RULES = {
    "wifi": "Network",
    "login": "IT Support",
    "software": "Applications",
    "hardware": "Infrastructure",
    "other": "General"
}

# SLA hours
SLA_RULES = {
    "High": 4,
    "Medium": 24,
    "Low": 72
}

PROCESSED_FILE = "processed_tickets.csv"
REJECTED_FILE = "rejected_tickets.csv"

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, str(email))

def generate_ticket_id():
    return "TICKET-" + str(uuid.uuid4())[:8]

def normalize(text):
    return str(text).strip().lower()

def load_existing(file):
    if os.path.exists(file):
        return pd.read_csv(file)
    return pd.DataFrame()

def save_ticket(file, ticket):
    df = load_existing(file)
    df = pd.concat([df, pd.DataFrame([ticket])], ignore_index=True)
    df.to_csv(file, index=False)

def check_duplicate(email, issue, timestamp):

    df = load_existing(PROCESSED_FILE)

    if df.empty:
        return False

    df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed")
    
    for _, row in df.iterrows():

        if row["email"] == email and row["issue_type"] == issue:
            diff = timestamp - row["timestamp"]

            if diff.total_seconds() < 86400:
                return True

    return False


def process_ticket(ticket):

    email = ticket["email"]
    priority = ticket["priority"]
    issue = normalize(ticket["issue_type"])
    timestamp = datetime.now()

    # Email validation
    if not validate_email(email):
        ticket["reason"] = "Invalid Email"
        save_ticket(REJECTED_FILE, ticket)
        return "Rejected", ticket

    # Priority validation
    if priority not in SLA_RULES:
        ticket["reason"] = "Invalid Priority"
        save_ticket(REJECTED_FILE, ticket)
        return "Rejected", ticket

    # Issue validation
    if issue not in ROUTING_RULES:
        ticket["reason"] = "Unknown Issue Type"
        save_ticket(REJECTED_FILE, ticket)
        return "Rejected", ticket

    # Deduplication
    if check_duplicate(email, issue, timestamp):
        ticket["reason"] = "Duplicate Ticket within 24h"
        save_ticket(REJECTED_FILE, ticket)
        return "Rejected", ticket

    ticket_id = generate_ticket_id()
    team = ROUTING_RULES[issue]

    sla_deadline = timestamp + timedelta(hours=SLA_RULES[priority])

    processed_ticket = {
        "ticket_id": ticket_id,
        "name": ticket["name"],
        "email": email,
        "issue_type": issue,
        "priority": priority,
        "description": ticket["description"],
        "assigned_team": team,
        "timestamp": timestamp,
        "sla_deadline": sla_deadline
    }

    save_ticket(PROCESSED_FILE, processed_ticket)

    return "Processed", processed_ticket


def generate_summary():

    processed = load_existing(PROCESSED_FILE)
    rejected = load_existing(REJECTED_FILE)

    summary = {
        "Total Tickets Received": len(processed) + len(rejected),
        "Processed Tickets": len(processed),
        "Rejected Tickets": len(rejected)
    }

    if not processed.empty:
        team_counts = processed["assigned_team"].value_counts()

        for team, count in team_counts.items():
            summary[f"{team} Tickets"] = count

    df = pd.DataFrame(list(summary.items()), columns=["Metric","Value"])
    df.to_csv("summary_report.csv", index=False)

    return df