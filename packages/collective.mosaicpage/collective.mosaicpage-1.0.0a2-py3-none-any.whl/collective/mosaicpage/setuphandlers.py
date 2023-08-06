from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import getUtility
from zope.interface import implementer

import logging


try:
    from plone.base.interfaces import INonInstallable
except ImportError:
    # BBB for Plone 5.2
    from Products.CMFPlone.interfaces import INonInstallable


logger = logging.getLogger(__name__)


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "collective.mosaicpage:uninstall",
        ]

    def getNonInstallableProducts(self):
        """Hide the upgrades package from site-creation and quickinstaller."""
        return ["collective.mosaicpage.upgrades"]


def post_install(context):
    """Post install script

    Remove the layout behaviors and view methods from all other FTIs.
    """
    types_tool = api.portal.get_tool(name="portal_types")

    layout_views = {"layout_view", "@@layout_view"}
    layout_behaviors = {
        "plone.app.blocks.layoutbehavior.ILayoutAware",
        "plone.layoutaware",
    }
    # Iterate through all Dexterity content type
    for fti in types_tool.listTypeInfo():
        behaviors = getattr(fti, "behaviors", None)
        if not behaviors:
            # not a Dexterity FTI
            continue
        fti_name = fti.__name__
        if fti_name == "MosaicPage":
            continue

        # Remove layout behaviors.
        if layout_behaviors & set(behaviors):
            fti.behaviors = tuple(
                [behavior for behavior in behaviors if behavior not in layout_behaviors]
            )
            logger.info("Removed layout behaviors from portal_type %s.", fti_name)

        # Remove layout views.
        if layout_views & set(fti.view_methods):
            fti.view_methods = tuple(
                [vm for vm in fti.view_methods if vm not in layout_views]
            )
            logger.info("Removed layout views from portal_type %s.", fti_name)

        # Update default view if needed.
        allowed_views = fti.view_methods
        if "view" in allowed_views:
            fallback_view = "view"
        else:
            fallback_view = allowed_views[0]
        if fti.default_view and fti.default_view in layout_views:
            fti.default_view = fallback_view
            logger.info(
                "Updated default view of portal_type %s to %s.",
                fti_name,
                fti.default_view,
            )

        # Update immediate (or initial) view if needed.
        if fti.immediate_view and fti.immediate_view in layout_views:
            fti.immediate_view = fti.default_view or fallback_view
            logger.info(
                "Updated immediate view of portal_type %s to %s.",
                fti_name,
                fti.immediate_view,
            )

        # Set the layout on content items if they had a layout view so far.
        catalog = api.portal.get_tool(name="portal_catalog")
        for layout_view in layout_views:
            for brain in catalog.unrestrictedSearchResults(
                layout=layout_view, portal_type=fti_name
            ):
                try:
                    obj = brain.getObject()
                except (KeyError, AttributeError):
                    logger.warning("Could not get object at path %s", brain.getPath())
                    continue
                if obj.hasProperty("layout"):
                    obj.manage_delProperties(["layout"])
                    logger.info("Removed layout property from %s", brain.getPath())
                obj.reindexObject(idxs=["layout"])


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
