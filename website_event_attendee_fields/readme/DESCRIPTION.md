By default `website_event` module asks only three fields to fill about attendees (name, email, phone). This module allows to customize any set of fields.

Also,

* if total bootstrap width of field columns is more that 12

  - hides Header at Attendee form
  - shows field name above each input

* If user is authenticated:

  - first attendee at the form will have autofilled values (if person is not registered yet)

* Modifies behaviour of `partner_event` module:

  - always updates Registration's name and phone to corresponded values of Attendee Partner, because they may be taken from Partner record (e.g. Public User)

  - If attendee partner exists and current (authenticated) user is the attendee partner himself: update partner values. (We don't update fields always, because it leads to security issue: anyone can change partner name, passport, etc. just knowing his email). Default behaviour: only create partner if one doesn't exist.

* Prevents changing qty for event lines (TODO: move this to a separate module)
* Custom redirection after filling ticket form, e.g. to cart page to ask for coupons (TODO: move this to a separate module). Create System Parameter `website_event_sale.redirection` to configure it.
