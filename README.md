# Toggle Remaining Card Count

**AnkiWeb Page: https://ankiweb.net/shared/info/1489494509**

![Screenshot of remaining card count in Anki](remaining_card_count.png)

This add-on allows you to toggle visibility of the Remaining Card Count (pictured above) using either a keyboard shortcut or an Anki Menu Bar item.

The default keyboard shortcut is the backtick/grave accent key (`), which is to the left of the number "1" on the US QWERTY keyboard. This shortcut can be configured in the add-on's config JSON.

## Configuration
### Keyboard Shortcut (`shortcut`)
To change the keyboard shortcut, open Tools > Add-ons, then select this add-on and click the "Config" button. For example, the following configuration:
```json
{
    "method": "preferences",
    "shortcut": "Ctrl+Shift+8"
}
```
will change the keyboard shortcut to `Ctrl`+`Shift`+`8` (`Cmd`+`Shift`+`8` on Mac).

### Toggling Method (`method`)
By default, this add-on works by toggling the built-in Anki preference for showing the Remaining Card Count. Each time the preference is changed, Anki refreshes the current deck. This can cause odd behavior, such as a Learning-phase card being pushed to the front of the deck and replacing a Review-phase card that was just on the screen.<br>
<br>
This add-on can circumvent this behavior by showing/hiding the Remaining Card Count using a web-based method instead of using Anki preferences. To enable this, use `"method": "web"` in the add-on's config, e.g.:
```json
{
    "method": "web",
    "shortcut": "`"
}
```
NOTE: If using the `web` method, then **you must <u>enable</u> the Anki Preference for the showing Remaining Card Count</u>**!
