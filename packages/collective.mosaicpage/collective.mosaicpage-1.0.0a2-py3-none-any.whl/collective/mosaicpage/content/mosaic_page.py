from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IMosaicPage(model.Schema):
    """Marker interface and Dexterity Python Schema for MosaicPage"""


@implementer(IMosaicPage)
class MosaicPage(Container):
    """Content-type class for IMosaicPage"""
