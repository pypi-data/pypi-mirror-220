from typing import TYPE_CHECKING

from twisted.plugin import IPlugin
from zope.interface import implementer

from ..plugin import BasePyFSDPlugin, PreventEvent

if TYPE_CHECKING:
    from ..protocol.client import FSDClientProtocol
    from ..service import PyFSDService


@implementer(IPlugin)
class TestrPlugin(BasePyFSDPlugin):
    plugin_name = "testr"

    def beforeStart(self, pyfsd: "PyFSDService", config) -> None:
        self.pyfsd = pyfsd
        print(config)

    def lineReceivedFromClient(
        self, protocol: "FSDClientProtocol", byte_line: bytes
    ) -> None:
        protocol.sendLine(b"I heard: " + byte_line)
        raise PreventEvent


# testr = TestrPlugin()
