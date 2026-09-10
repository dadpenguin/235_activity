from utils.user import generate_random_user_id


def test_generate_random_user_id_returns_integer():
    user_id = generate_random_user_id()

    assert isinstance(user_id, int)


def test_generate_random_user_id_is_four_digits():
    user_id = generate_random_user_id()

    assert 1000 <= user_id <= 9999


def test_generate_random_user_id_multiple_times():
    for _ in range(100):
        user_id = generate_random_user_id()

        assert isinstance(user_id, int)
        assert 1000 <= user_id <= 9999