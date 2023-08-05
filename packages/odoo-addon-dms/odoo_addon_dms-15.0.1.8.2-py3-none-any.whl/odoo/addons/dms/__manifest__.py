# Copyright 2017-2019 MuK IT GmbH
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Document Management System",
    "summary": """Document Management System for Odoo""",
    "version": "15.0.1.8.2",
    "category": "Document Management",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/dms",
    "author": "MuK IT, Tecnativa, Odoo Community Association (OCA)",
    "depends": [
        "web_drop_target",
        "mail",
        "http_routing",
        "portal",
        "mail_preview_base",
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "actions/file.xml",
        "template/onboarding.xml",
        "views/menu.xml",
        "views/tag.xml",
        "views/category.xml",
        "views/dms_file.xml",
        "views/directory.xml",
        "views/storage.xml",
        "views/dms_access_groups_views.xml",
        "views/res_config_settings.xml",
        "views/dms_portal_templates.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "dms/static/src/scss/variables.scss",
            "dms/static/src/scss/file_kanban.scss",
            "dms/static/src/scss/directory_kanban.scss",
            "dms/static/src/js/fields/path.js",
            "dms/static/src/js/views/many_drop_target.js",
            "dms/static/src/js/views/search_panel.esm.js",
            "dms/static/src/js/views/file_list_controller.js",
            "dms/static/src/js/views/file_list_view.js",
            "dms/static/src/js/views/file_kanban_controller.js",
            "dms/static/src/js/views/file_kanban_renderer.js",
            "dms/static/src/js/views/file_kanban_view.js",
        ],
        "web.assets_qweb": ["dms/static/src/xml/views.xml"],
        "web.assets_frontend": ["dms/static/src/js/dms_portal_tour.js"],
    },
    "demo": [
        "demo/res_users.xml",
        "demo/access_group.xml",
        "demo/category.xml",
        "demo/tag.xml",
        "demo/storage.xml",
        "demo/directory.xml",
        "demo/file.xml",
    ],
    "images": ["static/description/banner.png"],
    "application": True,
}
