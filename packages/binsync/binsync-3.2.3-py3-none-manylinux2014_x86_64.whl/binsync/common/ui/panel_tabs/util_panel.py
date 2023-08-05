import logging

from binsync.common.controller import BinSyncController, MergeLevel
from binsync.common.ui.qt_objects import (
    QCheckBox,
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    Qt,
    QVBoxLayout,
    QWidget,
)
from binsync.common.ui.magic_sync_dialog import MagicSyncDialog
from binsync.common.ui.force_push import ForcePushUI
from binsync.common.controller import BinSyncController
from binsync.core.scheduler import SchedSpeed

l = logging.getLogger(__name__)


class QUtilPanel(QWidget):
    def __init__(self, controller: BinSyncController, parent=None):
        super().__init__(parent)
        self.controller = controller
        self._init_widgets()

    def _init_widgets(self):

        #
        # Developer Options Group
        #

        dev_options_group = QGroupBox()
        dev_options_layout = QVBoxLayout()
        dev_options_group.setTitle("Developer Options")
        dev_options_group.setLayout(dev_options_layout)

        self._debug_log_toggle = QCheckBox("Toggle Debug Logging")
        self._debug_log_toggle.setToolTip("Toggles the logging of events BinSync developers care about.")
        self._debug_log_toggle.stateChanged.connect(self._handle_debug_toggle)
        dev_options_layout.addWidget(self._debug_log_toggle)

        #
        # Sync Options Group
        #

        sync_options_group = QGroupBox()
        sync_options_layout = QVBoxLayout()
        sync_options_group.setTitle("Sync Options")
        sync_options_group.setLayout(sync_options_layout)

        self._merge_level_label = QLabel("Sync Merge Level")
        self._merge_level_label.setToolTip(
            """<html>
            <p>
            Defines which method is used to sync artifacts from another user.<br>
            <b>Non-Conflicting</b>: Only syncs artifacts that are not currently defined by you, so nothing is ever overwritten.<br>
            <b>Overwrite</b>: Syncs all artifacts regardless of your defined ones, overwriting everything.<br>
            <b>Merge</b>: You pick which artifacts are synced via the UI. <b>Unimplemented.</b>
            </p>
            </html>
            """)
        self._merge_level_label.setTextFormat(Qt.RichText)
        self._merge_level_combobox = QComboBox()
        self._merge_level_combobox.addItems(["Non-Conflicting", "Overwrite", "Merge"])
        self._merge_level_combobox.currentIndexChanged.connect(self._handle_sync_level_change)

        sync_level_layout = QHBoxLayout()
        #sync_level_group.layout().setContentsMargins(0, 0, 0, 0)
        sync_level_layout.addWidget(self._merge_level_label)
        sync_level_layout.addWidget(self._merge_level_combobox)

        self._magic_sync_button = QPushButton("Initiate Magic Sync")
        self._magic_sync_button.clicked.connect(self._handle_magic_sync_button)
        self._magic_sync_button.setToolTip("Performs a best effort merge of all existing user data to your state, "
                                           "but won't affect your existing state (this uses a non-conflicting merge).")

        self._force_push_button = QPushButton("Force Push...")
        self._force_push_button.clicked.connect(self._handle_force_push_button)
        self._force_push_button.setToolTip("Manually select function and globals you would like to be force committed "
                                           "and pushed to your user branch on Git.")

        sync_options_layout.addLayout(sync_level_layout)
        sync_options_group.layout().addWidget(self._magic_sync_button)
        sync_options_group.layout().addWidget(self._force_push_button)

        #
        # Final Layout
        #

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 20, 10, 20)
        main_layout.setSpacing(18)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.addWidget(sync_options_group)
        main_layout.addWidget(dev_options_group)
        self.setLayout(main_layout)

    #
    # Event Handlers
    #

    def _handle_debug_toggle(self):
        if self._debug_log_toggle.isChecked():
            logging.getLogger("binsync").setLevel("DEBUG")
            logging.getLogger("ida_binsync").setLevel("DEBUG")
            l.info("Logger has been set to level: DEBUG")
        else:
            logging.getLogger("binsync").setLevel("INFO")
            logging.getLogger("ida_binsync").setLevel("INFO")
            l.info("Logger has been set to level: INFO")

    def _handle_sync_level_change(self, index):
        selected_opt = self._merge_level_combobox.itemText(index)
        if selected_opt == "Non-Conflicting":
            self.controller.merge_level = MergeLevel.NON_CONFLICTING
        elif selected_opt == "Overwrite":
            self.controller.merge_level = MergeLevel.OVERWRITE
        elif selected_opt == "Merge":
            self.controller.merge_level = MergeLevel.MERGE
        else:
            return
        l.debug(f"Sync level changed to: {selected_opt}")

    def _handle_magic_sync_button(self):
        dialog = MagicSyncDialog(self.controller)
        dialog.exec_()

        if not dialog.should_sync:
            return

        self.controller.magic_fill(preference_user=dialog.preferred_user)

    def _handle_force_push_button(self):
        self.popup = ForcePushUI(self.controller)
        self.popup.show()
