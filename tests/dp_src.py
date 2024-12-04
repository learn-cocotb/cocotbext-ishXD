import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer
from cocotb.handle import SimHandle
from typing import List, Any
import sys

sys.path.append("./src/cocotb_vip_templates")
from monitor import MainLinkMonitor


@cocotb.test()
async def tb_data_stream(dut: SimHandle) -> None:

    dut.tx_symbol_clk.value = 0
    dut.tx_align_train.value = 0
    dut.tx_clock_train.value = 0
    dut.tx_link_established.value = 1

    clock: Clock = Clock(dut.tx_symbol_clk, 8, units="ns")  # 125MHz clock
    cocotb.start_soon(clock.start())

    # Signals to monitor
    test_signal_ready: SimHandle = dut.test_signal_ready
    tx_symbols: SimHandle = dut.tx_symbols

    # List to store received transactions
    received_data: List[Any] = []

    def monitor_callback(transaction: Any) -> None:
        """Callback function for the monitor to process received transactions.

        Args:
            transaction (Any): The transaction data captured by the monitor.
        """
        received_data.append(transaction)

    monitor: MainLinkMonitor = MainLinkMonitor(dut, callback=monitor_callback)
    await Timer(1, units="ms")

  
    count: int = 0
    while count < 1000:
        await ClockCycles(dut.tx_symbol_clk, 1)  
        count += 1

    assert int(test_signal_ready.value) == 1, f"Test signal not ready after {count} cycles"
    assert tx_symbols.value is not None, "tx_symbols should not be None"
