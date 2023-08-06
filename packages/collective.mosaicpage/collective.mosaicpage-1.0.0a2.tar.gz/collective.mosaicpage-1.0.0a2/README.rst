=====================
collective.mosaicpage
=====================

A page with Mosaic selected as only layout

Features
--------

- Adds a portal_type MosaicPage.
- This is a Container, where you can add Images.
- The ``layout_view`` from ``plone.app.mosaic`` is the only possible layout.
- On install, the layout behaviors and views are removed from all other portal types.
  We remove the layout property from all content items that have ``layout_view`` as layout:
  they will use the default view again.
- Only Manager and Site Administrator can add MosaicPages.
  Editors can still edit them.


Installation
------------

Install collective.mosaicpage by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.mosaicpage


and then running ``bin/buildout``.


Contribute
----------

If you are having issues, or want to contribute a bugfix or feature, please let us know.

- Issue Tracker: https://github.com/collective/collective.mosaicpage/issues
- Source Code: https://github.com/collective/collective.mosaicpage


License
-------

The project is licensed under the GPLv2.
