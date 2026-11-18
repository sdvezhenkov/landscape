from app.tools.essential.collections.inverse.inverse import inverse


def test_inverse():
    passed_dict = {
        'a': 1,
        'b': 2,
        'c': 3,
    }
    expected_dict = {
        1: 'a',
        2: 'b',
        3: 'c',
    }
    inversed_dict = inverse(passed_dict)
    assert inversed_dict == expected_dict
