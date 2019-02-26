from . import TestConfig, AbstractTest


class TestServiceIsUp(AbstractTest):
    """
    Check that server is alive and returning login view
    """
    def test_login_view(self):
        self.driver.get(f"{TestConfig.SERVER_URL}:{TestConfig.SERVER_PORT}")
        self.assertEqual(self.driver.title, "Sign in")

