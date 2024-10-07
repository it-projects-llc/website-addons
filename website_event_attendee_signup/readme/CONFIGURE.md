* At `Events` menu create or select existing event
* Switch **[x] Signup attendees to portal** on
* Switch **[x] Create Partners in registration** on
* At `Email Schedule` add a line:

  - **Email to Send**:  *Event: Signup*
  - **Unit**: *Immediately*
  - **When to Run**: *After each registration*

Alternative email template configuration:

* Activate Developer Mode
* Open menu `[[ Settings ]] >> Technical >> Email >> Templates`
* Filter out records by keyword *Event*
* Open *Event: Signup* record
* Click `[Edit]`
* Click icon `</>` to switch to Code view
* Copy the code related to signup
* Go back to templates
* Open *Event: Reminder* record
* Click `[Edit]`
* Click icon `</>` to switch to Code view
* Paste the copied code
* Click `[Save]`
