from aqt import mw
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtCore import Qt
from aqt.qt import qconnect
from aqt.operations.collection import set_preferences
from aqt.utils import showInfo

from aqt import operations
from aqt.operations import ResultWithChanges
from concurrent.futures._base import Future

def toggle_count():
    # Only support toggling when a question/card is on-screen (ensure ease buttons are present)
    if mw.reviewer.state != "question" or not mw.reviewer.card:
        return

    # Derived from https://github.com/ankitects/anki/blob/1be94a8b0461defcbf2a2d39e5a1f316446b0169/qt/aqt/preferences.py#L153
    prefs = mw.col.get_preferences()
    prefs.reviewing.show_remaining_due_counts = not prefs.reviewing.show_remaining_due_counts
    collection_op = set_preferences(parent=mw, preferences=prefs)

    # Derived from https://github.com/ankitects/anki/blob/64ca90934bc26ddf7125913abc9dd9de8cb30c2b/qt/aqt/operations/__init__.py#L99
    # Redraws bottom bar ONLY
    assert mw
    mw._increase_background_ops()

    def wrapped_op() -> ResultWithChanges:
        assert mw
        return collection_op._op(mw.col)

    def wrapped_done(future: Future) -> None:
        assert mw
        mw._decrease_background_ops()
        # did something go wrong?
        if exception := future.exception():
            if isinstance(exception, Exception):
                operations.show_exception(parent=collection_op._parent, exception=exception)
                return
            else:
                # BaseException like SystemExit; rethrow it
                future.result()

        result = future.result()
        mw.reviewer._showAnswerButton()

    collection_op._run(mw, wrapped_op, wrapped_done)

def init():
    config = mw.addonManager.getConfig(__name__)

    key_seq = QKeySequence('`')  # default
    if config is not None and "shortcut" in config and config['shortcut']:
        key_seq = QKeySequence(config['shortcut'])
        if key_seq.matches(Qt.Key.Key_unknown) != QKeySequence.SequenceMatch.NoMatch:
            showInfo(f"WARNING: The configured keyboard shortcut for the Toggle Remaining Card Count add-on is invalid! Please double-check the configuration under Tools > Add-Ons.")
            return

    action = QAction("Toggle Remaining Card Count", mw)
    qconnect(action.triggered, toggle_count)
    action.setShortcut(QKeySequence(key_seq))
    mw.form.menuTools.addAction(action)

init()
