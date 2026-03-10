# Automated Ticket Processing System

## Project Overview

This project is an **Automated Ticket Processing System** developed using **Python** and **Streamlit**.
The system automates the process of receiving, validating, routing, and managing support tickets. It also generates reports for tracking ticket status and operational performance.

The goal of this project is to simulate a **basic helpdesk automation workflow** where incoming tickets are processed and assigned to the appropriate support teams.

---

## Features

* Add new support tickets through a web interface
* Upload multiple tickets using a CSV file
* Validate ticket information (email format, issue type, required fields)
* Detect duplicate tickets
* Automatically route tickets to the correct support team
* Assign SLA (Service Level Agreement) based on priority
* Store processed tickets
* Store rejected tickets with error reasons
* Generate a summary report in CSV format

---

## Technology Stack

* **Python**
* **Streamlit** – Web interface
* **Pandas** – Data processing
* **CSV** – Data storage and reporting

---

## Ticket Processing Workflow

1. User submits a ticket through the form or uploads a CSV file.
2. The system validates the ticket information:

   * Email format
   * Required fields
   * Valid issue type
3. Duplicate tickets are detected.
4. Valid tickets are routed to the appropriate support team.
5. SLA is assigned based on ticket priority.
6. Processed tickets are saved to `processed_tickets.csv`.
7. Invalid tickets are stored in `rejected_tickets.csv`.
8. A summary report is generated.

---

## Issue Type Routing Logic

| Issue Type | Assigned Team    |
| ---------- | ---------------- |
| wifi       | Network Team     |
| login      | IT Support       |
| software   | Software Support |
| hardware   | Hardware Support |

---

## SLA Assignment

| Priority | SLA      |
| -------- | -------- |
| High     | 4 Hours  |
| Medium   | 8 Hours  |
| Low      | 24 Hours |

---

## Project Structure

```
project-folder/
│
├── app.py
├── ticket_automation.py
├── tickets_test.csv
├── processed_tickets.csv
├── rejected_tickets.csv
├── summary_report.csv
└── README.md
```

---

## Installation

### 1. Create Environment (Optional)

```bash
conda create -n ticket_env python=3.10
conda activate ticket_env
```

### 2. Install Dependencies

```bash
pip install streamlit pandas
```

---

## Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## Testing the System

### Add Ticket

Use the **Add Ticket** form in the UI to submit a ticket manually.

### Upload CSV

Upload a CSV file containing multiple tickets.

Example CSV format:

```
name,email,issue_type,priority,description
Rahul,rahul@gmail.com,wifi,High,Wifi not working
Amit,amit@gmail.com,login,Medium,Login issue
Sara,sara@gmail.com,hardware,Low,Laptop not starting
```

---

## Output Files

### Processed Tickets

`processed_tickets.csv`

Contains successfully processed tickets.

### Rejected Tickets

`rejected_tickets.csv`

Contains invalid or duplicate tickets with rejection reasons.

### Summary Report

`summary_report.csv`

Includes:

* Total tickets received
* Processed tickets
* Rejected tickets
* Tickets per team

---

## Example Summary Report

| Metric        | Value |
| ------------- | ----- |
| Total Tickets | 50    |
| Processed     | 42    |
| Rejected      | 8     |

---

## Future Improvements

* Database integration (PostgreSQL / MySQL)
* Email notifications
* Ticket dashboard analytics
* LLM-based issue classification
* Integration with helpdesk platforms

---

## Author

**Chintan Dabhi**

MCA (AI & ML) Student
Interested in AI, Automation, and Generative AI Systems.
