from pathlib import Path
import duckdb
import json
from datetime import datetime


class FraudAnalyzer:

    def __init__(self, db_path="fraud.db"):
        self.db_path = db_path
        self.conn = duckdb.connect(db_path)

    def _read_sql(self, filename):
        return Path("sql") / filename

    def run_velocity_check(self):
        query = Path("sql/velocity_fraud.sql").read_text()
        df = self.conn.execute(query).fetchdf()
        return df

    def run_geo_check(self):
        query = Path("sql/geo_fraud.sql").read_text()
        df = self.conn.execute(query).fetchdf()
        return df

    def run_amount_check(self):
        query = Path("sql/amount_deviation.sql").read_text()
        df = self.conn.execute(query).fetchdf()
        return df

    def run_all(self):

        print("Running velocity fraud check...")
        velocity_df = self.run_velocity_check()

        print("Running geo fraud check...")
        geo_df = self.run_geo_check()

        print("Running amount fraud check...")
        amount_df = self.run_amount_check()

        total_txns = self.conn.execute(
            "SELECT COUNT(*) FROM transactions"
        ).fetchone()[0]

        result = {
            "run_timestamp": datetime.utcnow().isoformat(),
            "total_transactions": total_txns,
            "summary": {
                "velocity_flags": len(velocity_df),
                "geo_flags": len(geo_df),
                "amount_flags": len(amount_df),
            },
            "velocity_flags": velocity_df.head(100).to_dict(orient="records"),
            "geo_flags": geo_df.head(100).to_dict(orient="records"),
            "amount_flags": amount_df.head(100).to_dict(orient="records"),
        }

        return result

    def export_findings(self, output_path="results/findings.json"):

        Path("results").mkdir(exist_ok=True)

        results = self.run_all()

        with open(output_path, "w") as f:
            json.dump(results, f, indent=4, default=str)

        print(f"Results exported to {output_path}")

        return output_path

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    analyzer = FraudAnalyzer()
    analyzer.export_findings()
    analyzer.close()