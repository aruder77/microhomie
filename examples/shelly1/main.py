import settings

from machine import Pin
from aswitch import Switch

from homie.node import HomieNode
from homie.device import HomieDevice
from homie.property import HomieNodeProperty
from homie.constants import TRUE, FALSE


class SmartSocket(HomieNode):
    def __init__(self):
        super().__init__(id="relay", name="Light switch", type="Shelly 1")
        self.relay = Pin(4, Pin.OUT, value=0)
        self.switch = Switch(Pin(5, Pin.IN))

        self.relay_property = HomieNodeProperty(
            id="power",
            name="Relay",
            settable=True,
            retained=True,
            datatype="boolean",
            default=FALSE,
            restore=True,
        )
        self.add_property(self.relay_property)

        self.switch.open_func(self.toggle, ())
        self.switch.close_func(self.toggle, ())

    def off(self):
        self.relay(0)
        self.relay_property.data = FALSE

    def on(self):
        self.relay(1)
        self.relay_property.data = TRUE

    def callback(self, topic, payload, retained):
        if b"power" in topic:
            if payload == FALSE:
                self.off()
            elif payload == TRUE:
                self.on()

    def toggle(self):
        if self.relay_property.data == TRUE:
            self.off()
        else:
            self.on()


def main():
    homie = HomieDevice(settings)
    homie.add_node(SmartSocket())
    homie.start()


if __name__ == "__main__":
    main()
