from fraud_analyzer import FraudAnalyzer


def test_full_pipeline(tmp_path):

    analyzer = FraudAnalyzer()

    output_file = tmp_path / "test_output.json"

    analyzer.export_findings(str(output_file))

    assert output_file.exists()

    analyzer.close()