The modules creates `res.user` from every `event.registration` (*attendee*)
and calls `signup_prepare()` method to allow to send an email with signup url to access the portal.

The modules adds email template `Event: Signup`, which can be used directly or as an example to modify other email template.
