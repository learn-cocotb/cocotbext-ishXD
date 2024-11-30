from cocotb_bus.monitors import BusMonitor, Monitor
from cocotb.triggers import RisingEdge


class MainLinkMonitor(BusMonitor):
    """Monitor for Main Link"""

    _signals = ["data", "ready"]

    def __init__(self, dut, callback=None, event=None):
        super().__init__(dut, None, dut.clk, callback=callback, event=event)

    async def _monitor_recv(self):
        """Capture data and ready signal values."""
        while True:
            await RisingEdge(self.clock)
            if self.bus.ready.value:
                self._recv(int(self.bus.data.value)) 


class AuxChannelMonitor(Monitor):
    """Monitor for the AUX channel protocol."""

    def __init__(self, signal, clk, callback=None, event=None):
        self.signal = signal  
        self.clock = clk     
        super().__init__(callback=callback, event=event)

    async def _monitor_recv(self):
        """Capture values from the AUX channel."""
        while True:
            await RisingEdge(self.clock)
            aux_data = self.signal.value.integer
            self._recv(aux_data)


            




