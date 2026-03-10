import streamlit as st
import pandas as pd
from ticket_automation import process_ticket, generate_summary

st.title("🎫 IT Support Ticket Automation System")

menu = st.sidebar.selectbox(
    "Menu",
    ["Add Ticket","Upload CSV Tickets","View Processed Tickets","View Rejected Tickets","Summary Report"]
)

# Add ticket UI
if menu == "Add Ticket":

    st.header("➕ Submit New Ticket")

    name = st.text_input("Name")
    email = st.text_input("Email")
    issue = st.selectbox("Issue Type",["wifi","login","software","hardware","other"])
    priority = st.selectbox("Priority",["High","Medium","Low"])
    description = st.text_area("Description")

    if st.button("Submit Ticket"):

        ticket = {
            "name": name,
            "email": email,
            "issue_type": issue,
            "priority": priority,
            "description": description
        }

        status, result = process_ticket(ticket)

        if status == "Processed":
            st.success("Ticket Processed Successfully")
            st.json(result)

        else:
            st.error("Ticket Rejected")
            st.json(result)

# Upload CSV
elif menu == "Upload CSV Tickets":

    st.header("📂 Upload Ticket CSV")

    file = st.file_uploader("Upload CSV", type=["csv"])

    if file:

        df = pd.read_csv(file)

        # Fix column names
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

        st.write("Detected columns:", df.columns)

        results = []

        for _, row in df.iterrows():

            ticket = {
                "name": row.get("name",""),
                "email": row.get("email",""),
                "issue_type": row.get("issue_type",""),
                "priority": row.get("priority",""),
                "description": row.get("description","")
            }

            status, result = process_ticket(ticket)

            results.append({
                "name": ticket["name"],
                "status": status,
                "message": result
            })

        st.success("CSV Processing Completed")

        result_df = pd.DataFrame(results)

        st.dataframe(result_df)

# Processed tickets
elif menu == "View Processed Tickets":

    st.header("✅ Processed Tickets")

    try:
        df = pd.read_csv("processed_tickets.csv")
        st.dataframe(df)
    except:
        st.info("No processed tickets yet")

# Rejected tickets
elif menu == "View Rejected Tickets":

    st.header("❌ Rejected Tickets")

    try:
        df = pd.read_csv("rejected_tickets.csv")
        st.dataframe(df)
    except:
        st.info("No rejected tickets yet")

# Summary
elif menu == "Summary Report":

    st.header("📑 Automation Summary")

    summary = generate_summary()

    st.dataframe(summary)

    st.download_button(
        "Download Summary CSV",
        summary.to_csv(index=False),
        "summary_report.csv"
    )