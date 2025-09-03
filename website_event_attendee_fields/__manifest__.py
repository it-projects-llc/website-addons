{
    "name": """Event guest Custom Field""",
    "summary": """Do you need more information about attendees than three default fields (name, email, phone)?""",  # noqa: E501
    "category": "Marketing",
    "images": ["images/banner.jpg"],
    "version": "17.0.1.0.0",
    "application": False,
    "author": "IT-Projects LLC",
    "support": "it@it-projects.info",
    "website": "https://github.com/it-projects-llc/website-addons",
    "license": "AGPL-3",
    "depends": ["website_event_sale", "partner_event"],
    "data": [
        "views/website_event_templates.xml",
        "views/event_event_views.xml",
        "views/event_question_views.xml",
        "views/event_templates_page_registration.xml",
        "views/ir_model_views.xml",
    ],
    "demo": [
        "data/event_event_demo.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_event_attendee_fields/static/src/js/registration_form.js",
        ],
        "web.assets_tests": [
            "website_event_attendee_fields/static/src/js/test_tour.js",
        ],
    },
}
