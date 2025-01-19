from aqt import mw
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtCore import Qt
from aqt.qt import qconnect
from aqt.operations.collection import set_preferences
from aqt.utils import showInfo

def toggle_remaining_card_count():
    # Derived from https://github.com/ankitects/anki/blob/1be94a8b0461defcbf2a2d39e5a1f316446b0169/qt/aqt/preferences.py#L153
    prefs = mw.col.get_preferences()
    prefs.reviewing.show_remaining_due_counts = not prefs.reviewing.show_remaining_due_counts
    set_preferences(parent=mw, preferences=prefs).run_in_background()

def init():
    config = mw.addonManager.getConfig(__name__)

    key_seq = QKeySequence('`')
    if config is not None:
        if "shortcut" in config and config['shortcut']:
            key_seq = QKeySequence(config['shortcut'])
            if key_seq.matches(Qt.Key.Key_unknown) != QKeySequence.SequenceMatch.NoMatch:
                showInfo(f"WARNING: The configured keyboard shortcut for the Toggle Remaining Card Count add-on is invalid! Please double-check the configuration under Tools > Add-Ons.")

    action = QAction("Toggle Remaining Card Count", mw)
    qconnect(action.triggered, toggle_remaining_card_count)
    action.setShortcut(QKeySequence(key_seq))
    mw.form.menuTools.addAction(action)

init()
