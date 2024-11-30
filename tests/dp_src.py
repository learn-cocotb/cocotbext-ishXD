import sys
sys.path.append('./src/cocotb_vip_templates')
from monitor import MainLinkMonitor

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ReadOnly, NextTimeStep, Timer


@cocotb.test()
async def test_source(dut):
    """Testbench for the tb_test_source wrapper."""
    clock = Clock(dut.clk, 8, units="ns")
    cocotb.start_soon(clock.start())

    received_data = []

    def monitor_callback(transaction):
        received_data.append(transaction)

    monitor = MainLinkMonitor(dut, callback=monitor_callback)
    await Timer(1, units="ms")

    # cocotb.log.info(f"Monitored data transactions: {received_data}")

    assert len(received_data) > 0, "No data transactions monitored."


