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
        "security/ir.model.access.csv",
        "views/assets.xml",
    ],
    "demo": [
        "data/event_event_attendee_field_demo.xml",
        "data/event_event_demo.xml",
        "views/assets_demo.xml",
    ],
}
