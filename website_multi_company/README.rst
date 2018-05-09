====================
 Real Multi Website
====================

Allows to set up multi-website and handles requests in a different company context. Later is especially useful for eCommerce to make orders for a different companies.

Odoo is designed to switch website by host name, but this feature is not completed and not supported. This module fills the gap.

Implementation
==============

Websites
--------

To work with ``website`` model, the module adds menu ``Website Admin >> Configuration >> Websites``.

To have unique home page per each website, the module makes duplicates of ``website.homepage``, e.g. ``website.homepage2`` for company #2.

To fix company logo (left side of top menu), the url is updated from ``/logo.png`` to ``/logo.png?company=ID``.

Website Menus
-------------

To easy work with ``website.menu`` model, the module adds menu ``Website Admin >> Configuration >> Website Menus`` and adds form view.

eCommerce
---------

Updates for eCommerce:

* ``/shop/*`` pages show only products for current company

Multi-Theme
-----------

* New menu to allow switch theme to multi-theme on-flight (i.e. without adding code to the theme).
* Removes `restrictions <https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module.py#L387-L400>`__ for Theme category, i.e. allows to install several themes at once

Roadmap
=======

* TODO: **Editor on websites** field should be hidden for not designers (if configuring user has no at least ``Restricted Editor`` in Website security)

Credits
=======

Contributors
------------
* Ivan Yelizariev <yelizariev@it-projects.info>

Sponsors
--------
* `IT-Projects LLC <https://it-projects.info>`__

Maintainers
-----------
* `IT-Projects LLC <https://it-projects.info>`__

Further information
===================

Demo: http://runbot.it-projects.info/demo/website-addons/10.0

HTML Description: https://apps.odoo.com/apps/modules/10.0/website_multi_company/

Usage instructions: `<doc/index.rst>`_

Changelog: `<doc/changelog.rst>`_

Notifications on updates: `via Atom <https://github.com/it-projects-llc/website-addons/commits/10.0/website_multi_company.atom>`_, `by Email <https://blogtrottr.com/?subscribe=https://github.com/it-projects-llc/website-addons/commits/10.0/website_multi_company.atom>`_

Tested on Odoo 10.0 ffba5c688ff74a0630f9f70be1d7760a43a7deba
