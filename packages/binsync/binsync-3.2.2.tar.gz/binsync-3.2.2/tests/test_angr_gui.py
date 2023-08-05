import os
import sys
import tempfile
import time
import unittest
import logging
from unittest.mock import patch

from PySide6.QtGui import QContextMenuEvent
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt, QPoint, QTimer
from PySide6.QtWidgets import QApplication, QMenu

import angr
from angrmanagement.ui.dialogs.rename_node import RenameNode
from angrmanagement.ui.main_window import MainWindow
from angrmanagement.config import Conf

from binsync.common.ui.version import set_ui_version
set_ui_version("PySide6")
from binsync.common.controller import SyncControlStatus
from binsync.common.ui import utils
from binsync.common.ui.config_dialog import SyncConfig

from common import timeout_after


app = None
test_location = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'binaries')
logging.disable(logging.CRITICAL)

BINSYNC_RELOAD_TIME = 10

#
# Test Utilities
#


def config_and_connect(binsync_plugin, username, sync_dir_path, init=False):
    config = SyncConfig(binsync_plugin.controller, open_magic_sync=False, load_config=not init)
    config._user_edit.setText("")
    config._repo_edit.setText("")
    QTest.keyClicks(config._user_edit, username)
    QTest.keyClicks(config._repo_edit, sync_dir_path)
    # always init for first user
    if init:
        QTest.mouseClick(config._initrepo_checkbox, Qt.MouseButton.LeftButton)

    QTest.mouseClick(config._ok_button, Qt.MouseButton.LeftButton)


def get_binsync_am_plugin(main_window):
    inactive_bs_plugin = main_window.workspace.plugins.loaded_plugins.get("binsync", None)
    if not inactive_bs_plugin:
        raise Exception("BinSync plugin is not present in AM plugins folder, or failed.")

    main_window.workspace.plugins.activate_plugin_by_name(inactive_bs_plugin.name.lower())
    binsync_plugin = main_window.workspace.plugins.active_plugins.get("binsync", None)
    if not binsync_plugin:
        raise Exception("Failed to activate BinSync plugin after load, probably because a newly"
                        " broken import. Break before activating and step through to find it.")

    return binsync_plugin


def start_am_gui(binpath):
    main = MainWindow(show=False)
    main.workspace.main_instance.project.am_obj = angr.Project(binpath, auto_load_libs=False)
    main.workspace.main_instance.project.am_event()
    main.workspace.main_instance.join_all_jobs()
    return main


def am_setUp():
    global app
    if app is None:
        app = QApplication([])
        Conf.init_font_config()
#
# Tests
#


class TestBinSyncPluginGUI(unittest.TestCase):
    """
    Unit Tests to test the BinSync Plugin for syncing across two users or more.
    Done inside angr-management decompiler.
    """

    def setUp(self):
        am_setUp()

    #
    # Helpers
    #
    def rename_function(self, main, func, new_function_name):
        """
        Renames a given function
        """
        disasm_view = main.workspace._get_or_create_disassembly_view()
        disasm_view._t_flow_graph_visible = True
        disasm_view.display_function(func)
        disasm_view.decompile_current_function()
        main.workspace.main_instance.join_all_jobs()
        pseudocode_view = main.workspace._get_or_create_pseudocode_view()
        for _, item in pseudocode_view.codegen.map_pos_to_node.items():
            if isinstance(item.obj, angr.analyses.decompiler.structured_codegen.c.CFunction):
                func_node = item.obj
                break
        else:
            self.fail("The CFunction _instance is not found.")
        rnode = RenameNode(code_view=pseudocode_view, node=func_node)
        rnode._name_box.setText("")
        QTest.keyClicks(rnode._name_box, new_function_name)
        QTest.mouseClick(rnode._ok_button, Qt.MouseButton.LeftButton)
        self.assertEqual(func.name, new_function_name)

    def rename_stack_variable(self, main, func, var_offset, new_var_name):
        """
        Renames a stack variable at a given function and offset
        """
        disasm_view = main.workspace._get_or_create_disassembly_view()
        disasm_view._t_flow_graph_visible = True
        disasm_view.display_function(func)
        disasm_view.decompile_current_function()
        main.workspace.main_instance.join_all_jobs()
        pseudocode_view = main.workspace._get_or_create_pseudocode_view()
        for _, item in pseudocode_view.codegen.map_pos_to_node.items():
            if isinstance(item.obj, angr.analyses.decompiler.structured_codegen.c.CVariable) and \
                    isinstance(item.obj.variable, angr.sim_variable.SimStackVariable) and \
                    item.obj.variable.offset == var_offset:
                var_node = item.obj
                break
        else:
            self.fail("The CVariable _instance is not found.")

        rnode = RenameNode(code_view=pseudocode_view, node=var_node)
        rnode._name_box.setText("")
        QTest.keyClicks(rnode._name_box, new_var_name)
        QTest.mouseClick(rnode._ok_button, Qt.MouseButton.LeftButton)

    def get_stack_variable(self, main, func, var_offset, var_man = None):
        """
        Gets a stack variable from a given function and offset
        """
        if var_man is None:
            var_man = main.workspace.main_instance.pseudocode_variable_kb.variables.get_function_manager(func.addr)
        for var in var_man._unified_variables:
            if isinstance(var, angr.sim_variable.SimStackVariable) and var.offset == var_offset:
                renamed_var = var
                break
        else:
            return None
        return renamed_var

    def click_sync_menu(self, table, obj_name):
        """
        Syncs from the first entry in a context menu for a given table and menu object name
        """
        table.contextMenuEvent(QContextMenuEvent(QContextMenuEvent.Mouse, QPoint(0, 0)))
        context_menu = next(
            filter(lambda x: isinstance(x, QMenu) and x.objectName() == obj_name,
                   QApplication.topLevelWidgets()))
        # triple check we got the right menu
        assert (context_menu.objectName() == obj_name)
        sync_action = next(filter(lambda x: x.text() == "Sync", context_menu.actions()))
        sync_action.trigger()

    def check_repo_update(self, binsync_plugin, user, func_name=None, func_addr=None):
        """
        Checks to ensure the repo has been updated correctly with either a function name or address
        """
        time.sleep(BINSYNC_RELOAD_TIME + BINSYNC_RELOAD_TIME // 2)
        control_panel = binsync_plugin.control_panel_view.control_panel
        top_change_func = list(control_panel._func_table.items.values())[0]
        top_change_activity = control_panel._activity_table.items[0]
        self.assertEqual(top_change_func.user, user)
        if func_name is not None:
            self.assertEqual(top_change_func.name, func_name)
        if func_addr is not None:
            self.assertEqual(top_change_activity.activity, func_addr)
        self.assertIsNot(top_change_func.last_push, None)
    #
    # Tests
    #

    @timeout_after
    def test_function_rename(self, timeout=2*60):
        binpath = os.path.join(test_location, "fauxware")
        new_function_name = "leet_main"
        user_1 = "user_1"
        user_2 = "user_2"
        with tempfile.TemporaryDirectory() as sync_dir_path:
            # ========= USER 1 =========
            # setup GUI
            main = start_am_gui(binpath)
            func = main.workspace.main_instance.project.kb.functions['main']
            self.assertIsNotNone(func)

            # find the binsync plugin and connect
            binsync_plugin = get_binsync_am_plugin(main)
            config_and_connect(binsync_plugin, user_1, sync_dir_path, init=True)
            self.assertEqual(binsync_plugin.controller.status(), SyncControlStatus.CONNECTED_NO_REMOTE)
            self.assertEqual(binsync_plugin.controller.client.master_user, user_1)

            # trigger a function rename in decompilation
            self.rename_function(main, func, new_function_name)

            # assure a new commit makes it to the repo
            self.check_repo_update(binsync_plugin, user_1, func_name=new_function_name)

            # reset the repo
            os.remove(sync_dir_path + "/.git/binsync.lock")

            # ========= USER 2 =========
            # setup GUI
            main = start_am_gui(binpath)
            func = main.workspace.main_instance.project.kb.functions['main']
            self.assertIsNotNone(func)

            # find the binsync plugin and connect
            binsync_plugin = get_binsync_am_plugin(main)
            config_and_connect(binsync_plugin, user_2, sync_dir_path)
            self.assertEqual(binsync_plugin.controller.status(), SyncControlStatus.CONNECTED_NO_REMOTE)
            self.assertEqual(binsync_plugin.controller.client.master_user, user_2)

            # wait for the control panel to get new data and force UI reload
            time.sleep(BINSYNC_RELOAD_TIME)
            control_panel = binsync_plugin.control_panel_view.control_panel
            control_panel.reload()

            # make a click event to sync new data from the first row in the table
            self.click_sync_menu(control_panel._func_table, "binsync_function_table_context_menu")

            # check to ensure function name synced properly
            self.assertEqual(func.name, new_function_name)
            
            controller = binsync_plugin.controller
            controller.stop_worker_routines()
            time.sleep(1)

            app.exit(0)

    @timeout_after
    def test_stack_variable_rename(self, timeout=2*60):
        binpath = os.path.join(test_location, "fauxware")
        var_offset = -0x18
        new_var_name = "leet_buff"
        user_1 = "user_1"
        user_2 = "user_2"

        with tempfile.TemporaryDirectory() as sync_dir_path:
            # ========= USER 1 =========
            # setup GUI
            main = start_am_gui(binpath)
            func = main.workspace.main_instance.project.kb.functions['main']
            old_name = func.name
            self.assertIsNotNone(func)

            # find the binsync plugin and connect
            binsync_plugin = get_binsync_am_plugin(main)
            config_and_connect(binsync_plugin, user_1, sync_dir_path, init=True)
            self.assertEqual(binsync_plugin.controller.status(), SyncControlStatus.CONNECTED_NO_REMOTE)
            self.assertEqual(binsync_plugin.controller.client.master_user, user_1)

            # trigger a variable rename in decompilation
            self.rename_stack_variable(main, func, var_offset, new_var_name)

            # check renamed variable
            var_man = main.workspace.main_instance.pseudocode_variable_kb.variables.get_function_manager(func.addr)
            self.assertEqual(self.get_stack_variable(main, func, var_offset, var_man).name, new_var_name)

            # assure a new commit makes it to the repo
            self.check_repo_update(binsync_plugin, user_1, func_addr=func.addr)

            # reset the repo
            os.remove(sync_dir_path + "/.git/binsync.lock")

            # ========= USER 2 =========
            # setup GUI
            main = start_am_gui(binpath)
            func = main.workspace.main_instance.project.kb.functions['main']
            self.assertIsNotNone(func)

            # find the binsync plugin and connect
            binsync_plugin = get_binsync_am_plugin(main)
            config_and_connect(binsync_plugin, user_2, sync_dir_path)
            self.assertEqual(binsync_plugin.controller.status(), SyncControlStatus.CONNECTED_NO_REMOTE)
            self.assertEqual(binsync_plugin.controller.client.master_user, user_2)

            # wait for the control panel to get new data and force UI reload
            time.sleep(BINSYNC_RELOAD_TIME)
            control_panel = binsync_plugin.control_panel_view.control_panel
            control_panel.reload()

            # assure functions did not change
            func_table = control_panel._func_table
            self.assertIsNotNone(list(func_table.items.values())[0].name)

            # make a click event to sync new data from the first row in the table
            self.click_sync_menu(control_panel._activity_table, "binsync_activity_table_context_menu")

            # assure function name did not change
            self.assertEqual(list(func_table.items.values())[0].name, "")
            self.assertEqual(func.name, old_name)

            # assure stack variable synced properly
            self.assertEqual(self.get_stack_variable(main, func, var_offset, var_man).name, new_var_name)

            controller = binsync_plugin.controller
            controller.stop_worker_routines()
            time.sleep(1)

            app.exit(0)


if __name__ == "__main__":
    unittest.main(argv=sys.argv)
