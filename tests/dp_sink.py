import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer
from cocotb_bus.monitors import Monitor
import sys
sys.path.append('./src/cocotb_vip_templates')
from monitor import AuxChannelMonitor

class DebugPMODMonitor(Monitor):
    """Monitor for the debug PMOD signals."""
    def __init__(self, signal, clk, callback=None, event=None):
        self.signal = signal
        self.clk = clk
        super().__init__(callback=callback, event=event)

    async def _monitor_recv(self):
        while True:
            await RisingEdge(self.clk)
            debug_data = self.signal.value.integer
            self._recv(debug_data)

@cocotb.test()
async def tb_dummy_sink_test(dut):
    """
    Testbench for tb_dummy_sink module.
    """
    clock = Clock(dut.clk100, 10, units="ns")  
    cocotb.start_soon(clock.start())

    dut.hotplug_detect.value = 0
    dut.sender_wr_en.value = 0
    dut.sender_wr_data.value = 0
    dut.sender_rd_en.value = 0
    dut.sender_abort.value = 0

    auxch_monitor = AuxChannelMonitor(dut.auxch_data, dut.clk100)
    debug_monitor = DebugPMODMonitor(dut.sender_debug_pmod, dut.clk100)

    auxch_data = []
    debug_data = []

    def collect_auxch_data(transaction):
        auxch_data.append(transaction)

    def collect_debug_data(transaction):
        debug_data.append(transaction)

    auxch_monitor.add_callback(collect_auxch_data)
    debug_monitor.add_callback(collect_debug_data)

    await Timer(100, units="ns")

    dut.hotplug_detect.value = 1
    await Timer(1, units="ms")


    # cocotb.log.info(f"Aux Channel Data: {auxch_data}")
    # cocotb.log.info(f"Debug PMOD Data: {debug_data}")


