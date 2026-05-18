def test_velocity_flags(test_db):

    query = open("sql/velocity_fraud.sql").read()

    df = test_db.execute(query).fetchdf()

    assert len(df) > 0
    assert "CARD_VELOCITY" in df["card_id"].values