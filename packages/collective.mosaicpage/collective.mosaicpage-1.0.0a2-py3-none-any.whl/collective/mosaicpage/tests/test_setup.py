"""Setup tests for this package."""
from collective.mosaicpage.testing import (  # noqa: E501
    COLLECTIVE_MOSAICPAGE_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


try:
    from plone.base.utils import get_installer
except ImportError:
    # BBB for Plone 5.2
    from Products.CMFPlone.utils import get_installer


class TestSetup(unittest.TestCase):
    """Test that collective.mosaicpage is properly installed."""

    layer = COLLECTIVE_MOSAICPAGE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if collective.mosaicpage is installed."""
        self.assertTrue(self.installer.is_product_installed("collective.mosaicpage"))

    def test_browserlayer(self):
        """Test that ICollectiveMosaicpageLayer is registered."""
        from collective.mosaicpage.interfaces import ICollectiveMosaicpageLayer
        from plone.browserlayer import utils

        self.assertIn(ICollectiveMosaicpageLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):
    layer = COLLECTIVE_MOSAICPAGE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("collective.mosaicpage")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.mosaicpage is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("collective.mosaicpage"))

    def test_browserlayer_removed(self):
        """Test that ICollectiveMosaicpageLayer is removed."""
        from collective.mosaicpage.interfaces import ICollectiveMosaicpageLayer
        from plone.browserlayer import utils

        self.assertNotIn(ICollectiveMosaicpageLayer, utils.registered_layers())
