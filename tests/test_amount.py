def test_amount_flags(test_db):

    query = open("sql/amount_deviation.sql").read()

    df = test_db.execute(query).fetchdf()

    assert len(df) > 0
    assert "CARD_AMOUNT" in df["card_id"].values