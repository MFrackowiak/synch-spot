from unittest import TestCase

from rpg_music.users.models import User


class UserTestCase(TestCase):
    def test_set_password(self):
        user = User("testowy")
        user.set_password("test1")
        self.assertEqual(
            user.password,
            "$pbkdf2-sha256$29000$YWRtISM0MzI1NDI1RSBXZGFzOSBpLTBBUzBkb2FzIGozbmZqams7bGFrZHNhZA$Jf0E5RZyWhminjvla8XRPHuiD1XRuukd3dB.tCE58K0",
        )

    def test_check_password(self):
        user = User("testowy")
        user.set_password("test1")
        self.assertTrue(user.check_password("test1"))
