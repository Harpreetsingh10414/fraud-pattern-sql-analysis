import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
import streamlit as st
import json
from fraud_analyzer import FraudAnalyzer
from pathlib import Path

st.set_page_config(page_title="Fraud Detection Dashboard", layout="wide")

st.title("🚨 Fraud Detection Dashboard")

# Run Analysis Button
if st.button("Run Analysis"):
    analyzer = FraudAnalyzer()
    analyzer.export_findings("results/findings.json")
    analyzer.close()
    st.success("Analysis completed!")

# Load JSON
if Path("results/findings.json").exists():
    with open("results/findings.json") as f:
        data = json.load(f)

    st.subheader("📊 Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Velocity Fraud", data["summary"]["velocity_flags"])
    col2.metric("Geo Fraud", data["summary"]["geo_flags"])
    col3.metric("Amount Fraud", data["summary"]["amount_flags"])

    st.subheader("📍 Velocity Fraud Transactions")
    st.dataframe(data["velocity_flags"])

    st.subheader("🌍 Geo Fraud Transactions")
    st.dataframe(data["geo_flags"])

    st.subheader("💰 Amount Fraud Transactions")
    st.dataframe(data["amount_flags"])
else:
    st.warning("Run analysis first.")