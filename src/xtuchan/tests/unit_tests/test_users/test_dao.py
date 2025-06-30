import pytest

from xtuchan.auth.dao import UsersDAO


@pytest.mark.parametrize("user_id, email, is_present", [
    (1, "user1@example.com", True),
    (2, "user2@test.org", True),
    (111, "don't@now.com", False)
])
async def test_find_user_by_id(user_id, email, is_present):
    user = await UsersDAO.find_by_id(user_id)

    if is_present:
        assert user
        assert user.email == email
        assert user.id == user_id
    else:
        assert not user
