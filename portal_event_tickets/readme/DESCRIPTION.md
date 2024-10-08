Allows to customers see tickets for events at Portal.

* Only confirmed tickets with attendee_partner_id as current user are shown

Additional features:

* Ticket transferring feature

  - To decrease chance of transferring to a wrong email, partner with the email must exist before transferring.
  - New *When to Run* values for Email Schedule:

    * transferring_started
    * transferring_finished

  - New attendee receives email with a link to finish ticket transferring

* Tracks changes in key registration fields (via `tracking=True`)

* Tickets can be changed to other products (including other tickets)

  - When old ticket is canceled, a message with a reference to new Sale Order is posted
