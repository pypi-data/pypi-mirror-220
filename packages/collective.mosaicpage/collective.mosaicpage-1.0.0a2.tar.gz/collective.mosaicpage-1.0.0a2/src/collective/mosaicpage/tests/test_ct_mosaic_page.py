# -*- coding: utf-8 -*-
from collective.mosaicpage.content.mosaic_page import IMosaicPage  # NOQA E501
from collective.mosaicpage.testing import (  # noqa
    COLLECTIVE_MOSAICPAGE_INTEGRATION_TESTING,
)
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class MosaicPageIntegrationTest(unittest.TestCase):
    layer = COLLECTIVE_MOSAICPAGE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.parent = self.portal

    def test_ct_mosaic_page_schema(self):
        fti = queryUtility(IDexterityFTI, name="MosaicPage")
        schema = fti.lookupSchema()
        self.assertEqual(IMosaicPage, schema)

    def test_ct_mosaic_page_fti(self):
        fti = queryUtility(IDexterityFTI, name="MosaicPage")
        self.assertTrue(fti)

    def test_ct_mosaic_page_factory(self):
        fti = queryUtility(IDexterityFTI, name="MosaicPage")
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IMosaicPage.providedBy(obj),
            "IMosaicPage not provided by {0}!".format(
                obj,
            ),
        )

    def test_ct_mosaic_page_adding(self):
        # Note: Contributor cannot add.
        setRoles(self.portal, TEST_USER_ID, ["Site Administrator"])
        obj = api.content.create(
            container=self.portal,
            type="MosaicPage",
            id="mosaic_page",
        )

        self.assertTrue(
            IMosaicPage.providedBy(obj),
            "IMosaicPage not provided by {0}!".format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn("mosaic_page", parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn("mosaic_page", parent.objectIds())

    def test_ct_mosaic_page_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ["Site Administrator"])
        fti = queryUtility(IDexterityFTI, name="MosaicPage")
        self.assertTrue(fti.global_allow, "{0} is not globally addable!".format(fti.id))

    def test_ct_mosaic_page_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ["Site Administrator"])
        fti = queryUtility(IDexterityFTI, name="MosaicPage")
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            "mosaic_page_id",
            title="MosaicPage container",
        )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type="Document",
                title="My Content",
            )
