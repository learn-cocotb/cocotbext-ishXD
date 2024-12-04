import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer
from cocotb.handle import SimHandle
from cocotb_bus.monitors import Monitor
from typing import List, Dict, Callable, Optional, Any
import sys

sys.path.append("./src/cocotb_vip_templates")


class DebugPMODMonitor(Monitor):
    """Monitor for the debug PMOD signals."""

    def __init__(self, signal: SimHandle, clk: SimHandle, callback: Optional[Callable[[Any], None]] = None, event: Optional[Any] = None) -> None:
        self.signal: SimHandle = signal
        self.clk: SimHandle = clk
        super().__init__(callback=callback, event=event)

    async def _monitor_recv(self) -> None:
        while True:
            await RisingEdge(self.clk)
            debug_data: int = self.signal.value.integer
            self._recv(debug_data)


async def drive_sender_abort(dut: SimHandle, value: int, delay_ns: int = 10) -> None:
    dut.sender_abort.value = value
    await Timer(delay_ns, units="ns")


async def drive_sender_data(dut: SimHandle, data_list: List[int], delay_ns: int = 10) -> None:
    for data in data_list:
        dut.sender_wr_data.value = data
        dut.sender_wr_en.value = 1
        await Timer(delay_ns, units="ns")
    dut.sender_wr_en.value = 0  
    await Timer(delay_ns, units="ns")


@cocotb.test()
async def test_edid_blocks(dut: SimHandle) -> None:

    cocotb.start_soon(Clock(dut.clk100, 10, units="ns").start())  # 100MHz clock

    dut.hotplug_detect.value = 0
    dut.sender_wr_en.value = 0
    dut.sender_wr_data.value = 0
    dut.sender_rd_en.value = 0
    dut.sender_abort.value = 0

    # EDID blocks for simulation
    edid_blocks: List[List[int]] = [
        [0x00, 0xD1, 0xC0, 0xD1, 0x00, 0x01, 0x01, 0xA3, 0x66, 0x00, 0xA0, 0xF0, 0x70, 0x1F, 0x80, 0x30, 0x20],
        [0x00, 0x35, 0x00, 0x6D, 0x55, 0x21, 0x00, 0x00, 0x1A, 0x00, 0x00, 0x00, 0xFF, 0x00, 0x55, 0x32, 0x4E],
        [0x00, 0x31, 0x34, 0x34, 0x31, 0x30, 0x30, 0x30, 0x38, 0x38, 0x0A, 0x00, 0x00, 0x00, 0xFC, 0x00, 0x56],
        [0x00, 0x58, 0x32, 0x38, 0x38, 0x30, 0x4D, 0x4C, 0x0A, 0x20, 0x20, 0x20, 0x20, 0x00, 0x00, 0x00, 0xFD],
        [0x00, 0x00, 0x18, 0x55, 0x1F, 0x72, 0x1E, 0x00, 0x0A, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x01, 0x42],
    ]

    # Replies for simulation
    replies: Dict[str, List[int]] = {
        "sink_count": [0x00, 0x01],
        "config_registers": [0x00, 0x11, 0x0A, 0xA4, 0x01, 0x01, 0x00, 0x01, 0x81, 0x00, 0x00, 0x00, 0x00],
        "8b10b_coding": [0x00],
        "link_bandwidth": [0x00],
        "downspread": [0x00],
        "lane_count": [0x00],
        "training_pattern": [0x00],
        "voltage_retry": [0x20],
        "voltage": [0x00],
        "link_status": [0x00, 0x00, 0x00, 0x01, 0x00, 0x80, 0x00, 0x00, 0x00],
        "link_adjust_request": [0x00, 0x00, 0x00],
        "training_pattern2": [0x00],
        "set_voltage2": [0x00],
        "link_status2": [0x00, 0x00, 0x00, 0x07, 0x00, 0x81, 0x00, 0x00, 0x00],
        "link_adjust2": [0x00, 0x00, 0x00],
        "training_pattern_off": [0x00]
    }

    # Simulate EDID blocks
    for block in edid_blocks:
        await drive_sender_abort(dut, 1)
        await drive_sender_abort(dut, 0)
        await drive_sender_data(dut, block)
        await Timer(300_000, units="ns")

    # Simulate replies
    for name, reply in replies.items():
        await drive_sender_abort(dut, 1)
        await drive_sender_abort(dut, 0)
        await drive_sender_data(dut, reply)
        await Timer(200_000, units="ns")

    dut._log.info("EDID blocks and replies simulated successfully.")
