# Example OpenCreator plugin module: [oc_hello] adds OC_HELLO and a status object.
#
# This file may be distributed under the terms of the GNU GPLv3 license.


class OCHello:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.greeting = config.get("greeting", "Hello from an OpenCreator plugin")
        self.count = 0
        gcode = self.printer.lookup_object("gcode")
        gcode.register_command("OC_HELLO", self.cmd_OC_HELLO,
                               desc="Say hello, with the active tool and its temperature")

    def cmd_OC_HELLO(self, gcmd):
        self.count += 1
        name = gcmd.get("NAME", None)
        eventtime = self.printer.get_reactor().monotonic()
        extruder = self.printer.lookup_object("toolhead").get_extruder()
        heater = extruder.get_status(eventtime)
        gcmd.respond_info("%s%s! Active extruder: %s at %.1f C (hello #%d)" % (
            self.greeting, ", " + name if name else "", extruder.get_name(),
            heater.get("temperature", 0.), self.count))

    def get_status(self, eventtime):
        return {"greeting": self.greeting, "count": self.count}


def load_config(config):
    return OCHello(config)
