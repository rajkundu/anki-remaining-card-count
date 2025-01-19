from aqt import mw
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtCore import Qt
from aqt.qt import qconnect
from aqt.operations.collection import set_preferences
from aqt.utils import showInfo

def toggle_count_via_preferences():
    # Derived from https://github.com/ankitects/anki/blob/1be94a8b0461defcbf2a2d39e5a1f316446b0169/qt/aqt/preferences.py#L153
    prefs = mw.col.get_preferences()
    prefs.reviewing.show_remaining_due_counts = not prefs.reviewing.show_remaining_due_counts
    set_preferences(parent=mw, preferences=prefs).run_in_background()

def toggle_count_via_web():
    mw.bottomWeb.eval("""
        var countWrapper = document.querySelector('.stattxt');
        if (countWrapper) {
            countWrapper.style.visibility = countWrapper.style.visibility === "hidden" ? "visible" : "hidden";
        }
    """)

def init():
    config = mw.addonManager.getConfig(__name__)

    key_seq = QKeySequence('`')  # default
    if config is not None and "shortcut" in config and config['shortcut']:
        key_seq = QKeySequence(config['shortcut'])
        if key_seq.matches(Qt.Key.Key_unknown) != QKeySequence.SequenceMatch.NoMatch:
            showInfo(f"WARNING: The configured keyboard shortcut for the Toggle Remaining Card Count add-on is invalid! Please double-check the configuration under Tools > Add-Ons.")
            return

    toggle_remaining_card_count = toggle_count_via_preferences # default
    if config is not None and "method" in config and config['method']:
        method = config['method'].lower().strip()
        if method == "web":
            toggle_remaining_card_count = toggle_count_via_web
        elif method == "preferences":
            pass # this is already the default
        else:
            showInfo(f"WARNING: 'method' for the Toggle Remaining Card Count add-on must be one of ('web', 'preferences')! Please double-check the configuration under Tools > Add-Ons.")
            return

    action = QAction("Toggle Remaining Card Count", mw)
    qconnect(action.triggered, toggle_remaining_card_count)
    action.setShortcut(QKeySequence(key_seq))
    mw.form.menuTools.addAction(action)

init()
