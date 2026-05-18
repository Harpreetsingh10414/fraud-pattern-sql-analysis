def test_geo_flags(test_db):

    query = open("sql/geo_fraud.sql").read()

    df = test_db.execute(query).fetchdf()

    assert len(df) > 0
    assert "CARD_GEO" in df["card_id"].values