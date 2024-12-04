from cocotb_bus.monitors import BusMonitor, Monitor
from cocotb.triggers import RisingEdge
from cocotb.handle import SimHandle
from typing import Optional, Callable, Any


class MainLinkMonitor(BusMonitor):
    """Monitor for Main Link."""

    _signals: list[str] = ["tx_symbols", "test_signal_ready"]

    def __init__(
        self, 
        dut: SimHandle, 
        callback: Optional[Callable[[int], None]] = None, 
        event: Optional[Any] = None
    ) -> None:
        """Initialize the Main Link Monitor.

        Args:
            dut (SimHandle): The device under test.
            callback (Optional[Callable[[int], None]]): Callback function for transactions.
            event (Optional[Any]): Event to trigger on a transaction.
        """
        super().__init__(dut, None, dut.tx_symbol_clk, callback=callback, event=event)

    async def _monitor_recv(self) -> None:
        """Capture data and ready signal values."""
        while True:
            await RisingEdge(self.clock)
            if self.bus.test_signal_ready.value:
                self._recv(int(self.bus.tx_symbols.value))


class AuxChannelMonitor(Monitor):
    """Monitor for the AUX channel protocol."""

    def __init__(
        self, 
        signal: SimHandle, 
        clk: SimHandle, 
        callback: Optional[Callable[[int], None]] = None, 
        event: Optional[Any] = None
    ) -> None:
        """Initialize the AUX Channel Monitor.

        Args:
            signal (SimHandle): The signal to monitor.
            clk (SimHandle): The clock signal.
            callback (Optional[Callable[[int], None]]): Callback function for transactions.
            event (Optional[Any]): Event to trigger on a transaction.
        """
        self.signal: SimHandle = signal
        self.clock: SimHandle = clk
        super().__init__(callback=callback, event=event)

    async def _monitor_recv(self) -> None:
        """Capture values from the AUX channel."""
        while True:
            await RisingEdge(self.clock)
            aux_data: int = self.signal.value.integer
            self._recv(aux_data)
