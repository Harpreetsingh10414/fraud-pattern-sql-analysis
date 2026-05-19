import sys
import json
from pathlib import Path
import streamlit as st

# Add project root to Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from fraud_analyzer import FraudAnalyzer


st.set_page_config(
    page_title="Fraud Detection Dashboard",
    layout="wide"
)

st.title("🚨 Fraud Detection Dashboard")

RESULT_PATH = ROOT_DIR / "results" / "findings.json"


# ---------------------------
# Run analysis
# ---------------------------

if st.button("Run Analysis"):

    try:
        analyzer = FraudAnalyzer()

        analyzer.export_findings(
            str(RESULT_PATH)
        )

        analyzer.close()

        st.success("Analysis completed!")

    except Exception as e:

        st.error(
            f"Analysis failed: {e}"
        )


# ---------------------------
# Display Results
# ---------------------------

if RESULT_PATH.exists():

    with open(RESULT_PATH) as f:
        data = json.load(f)

    st.subheader("📊 Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Velocity Fraud",
        data["summary"]["velocity_flags"]
    )

    col2.metric(
        "Geo Fraud",
        data["summary"]["geo_flags"]
    )

    col3.metric(
        "Amount Fraud",
        data["summary"]["amount_flags"]
    )


    st.divider()

    st.subheader("📍 Velocity Fraud")

    st.dataframe(
        data["velocity_flags"]
    )


    st.subheader("🌍 Geo Fraud")

    st.dataframe(
        data["geo_flags"]
    )


    st.subheader("💰 Amount Fraud")

    st.dataframe(
        data["amount_flags"]
    )

else:

    st.warning(
        "Run analysis first."
    )