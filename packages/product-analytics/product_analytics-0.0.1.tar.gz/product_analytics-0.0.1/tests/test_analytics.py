from peak_ai.analytics import replace_dynamic_value


def test_replace_dynamic_value():
    # Test replacing a number
    path = "prefix/12345/suffix"
    expected = "prefix/ID/suffix"
    actual = replace_dynamic_value(path)
    assert expected == actual

    # Test replacing a UUID
    path = "prefix/123e4567-e89b-12d3-a456-426614174000/suffix"
    expected = "prefix/ID/suffix"
    actual = replace_dynamic_value(path)
    assert expected == actual
