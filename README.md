# Fraud Pattern SQL Analysis

A production-style fraud detection pipeline built using SQL, DuckDB, and Python to detect real-world fraud patterns in financial transactions.

## Problem

Fraud detection in financial systems requires identifying abnormal transaction patterns in real time.

This project detects three key fraud patterns:

1. Velocity Fraud → Too many transactions in a short time window  
2. Geographic Fraud → Same card used in different cities within impossible time  
3. Amount Deviation → Transaction amount deviates from historical baseline  

## Architecture

```mermaid
flowchart LR
    A[Generate Data] --> B[DuckDB Database]
    B --> C[SQL Fraud Detection]
    C --> D[Python Analyzer]
    D --> E[JSON Output]
    E --> F[Streamlit Dashboard]


---

### 📁 Project Structure

```markdown
## Project Structure

fraud-pattern-sql-analysis/
│
├── sql/ # SQL fraud detection queries
├── data/ # Synthetic datasets
├── results/ # Output JSON
├── tests/ # pytest suite
│
├── generate_data.py
├── fraud_analyzer.py
├── README.md

## Setup

```bash
git clone <your-repo>
cd fraud-pattern-sql-analysis

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt


---

### 📊 Sample Output

```markdown
## Sample Output

```json
{
  "summary": {
    "velocity_flags": 1800,
    "geo_flags": 400,
    "amount_flags": 900
  }
}


---

### 🧠 Key Learnings

```markdown
## Key Learnings

- Advanced SQL window functions
- Fraud detection modeling
- Data pipeline orchestration
- Statistical anomaly detection
- Test-driven data engineering

## Tech Stack

- DuckDB
- Python
- Pandas
- Faker
- pytest
- Streamlit