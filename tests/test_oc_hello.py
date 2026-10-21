import importlib.util
import json
import pathlib
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("oc_hello", ROOT / "klippy" / "oc_hello.py")
oc_hello = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(oc_hello)


class FakeGCmd:
    def __init__(self, **params):
        self.params, self.replies = params, []

    def get(self, name, default=None):
        return self.params.get(name, default)

    def respond_info(self, msg):
        self.replies.append(msg)


class HelloTest(unittest.TestCase):
    def setUp(self):
        self.gcode = mock.Mock()
        extruder = mock.Mock()
        extruder.get_name.return_value = "extruder1"
        extruder.get_status.return_value = {"temperature": 215.04}
        toolhead = mock.Mock()
        toolhead.get_extruder.return_value = extruder
        printer = mock.Mock()
        printer.lookup_object.side_effect = {"gcode": self.gcode, "toolhead": toolhead}.get
        config = mock.Mock()
        config.get_printer.return_value = printer
        config.get.side_effect = lambda key, default=None: default
        self.hello = oc_hello.load_config(config)

    def test_registers_command(self):
        self.gcode.register_command.assert_called_once()
        self.assertEqual(self.gcode.register_command.call_args[0][0], "OC_HELLO")

    def test_replies_and_counts(self):
        cmd = FakeGCmd(NAME="Cart")
        self.hello.cmd_OC_HELLO(cmd)
        self.assertIn("Cart", cmd.replies[0])
        self.assertIn("extruder1 at 215.0 C", cmd.replies[0])
        self.assertEqual(self.hello.get_status(0.)["count"], 1)

    def test_manifest_files_exist(self):
        m = json.loads((ROOT / "opencreator-plugin.json").read_text())
        for rel in m["klippy_extras"] + m["moonraker_components"] + [m["klipper_config"], m["moonraker_config"]]:
            self.assertTrue((ROOT / rel).is_file(), rel)


if __name__ == "__main__":
    unittest.main()
