"""MainLinkBus."""
import cocotb
from cocotb_bus.bus import Bus as BusBaseClass
from cocotb.handle import SimHandle
from typing import List


class MainLinkBus:
    """Main Link Bus class for main link signals in DisplayPort."""

    def __init__(
        self,
        dut: SimHandle,
        prefix: str = "",
        suffix: str = "",
        bus_separator: str = "_",
        clk: str = "clk",
        reset: str = "rst_n",
        active_high_reset: bool = True,
        uppercase: bool = False,
    ) -> None:
        """Constructor for MainLinkBus.

        Args:
            dut (SimHandle): Device under test handle to access signals.
            prefix (str): Prefix for signal names in the bus.
            suffix (str): Suffix for signal names in the bus.
            bus_separator (str): Separator used in signal naming.
            clk (str): Clock signal name.
            reset (str): Reset signal name.
            active_high_reset (bool): If True, reset is active high; otherwise, active low.
            uppercase (bool): If True, convert bus signal names to uppercase.
        """
        self.dut: SimHandle = dut
        self.prefix: str = prefix
        self.suffix: str = suffix
        self.bus_separator: str = bus_separator
        self.clk: str = clk
        self.reset: str = reset
        self.active_high_reset: bool = active_high_reset
        self.uppercase: bool = uppercase
        self.bus: BusBaseClass = self.get_main_link_bus()

    def get_main_link_bus(self) -> BusBaseClass:
        """Creates and returns the main link bus object for DisplayPort transmission.

        This bus object includes signals for main link data transmission, handling
        raw data from the frame generator, processed data with MSA, and final data
        from the `test_source` module.

        Returns:
            BusBaseClass: The main link bus object for DisplayPort.
        """
        signals: List[str] = [  
            "stream_channel_count",
            "ready",
            "data",
            "tx_link_established",    
            "source_ready",                
            "tx_clock_train",             
            "tx_align_train",             
            "signal_data",                 
            "sr_inserted_data",            
            "scrambled_data",              
            "before_skew",                 
            "tx_symbols",  # Final data output after main stream processing               
        ]

        if self.uppercase:
            signals = [sig.upper() for sig in signals]
        signals = [f"{self.prefix}{self.bus_separator}{sig}{self.suffix}" for sig in signals]

        return BusBaseClass(
            dut=self.dut,
            name="",
            signals=signals,
            clk=self.clk,
            reset=self.reset
        )
