"""MainLinkBus."""
import cocotb
from cocotb_bus.bus import Bus as BusBaseClass


class MainLinkBus:
    """Main Link Bus class for main link signals in DisplayPort."""

    def __init__(
        self,
        dut: cocotb.SimHandle,
        prefix: str = "",
        suffix: str = "",
        bus_separator: str = "_",
        clk: str = "clk",
        reset: str = "rst_n",
        active_high_reset: bool = True,
        uppercase: bool = False,
    ):
        """Constructor for MainLinkBus.

        Args:
            dut (cocotb.SimHandle): Device under test handle to access signals.
            prefix (str): Prefix for signal names in the bus.
            suffix (str): Suffix for signal names in the bus.
            bus_separator (str): Separator used in signal naming.
            clk (str): Clock signal name.
            reset (str): Reset signal name.
            active_high_reset (bool): If True, reset is active high; otherwise, active low.
            uppercase (bool): If True, convert bus signal names to uppercase.
        """
        self.dut = dut
        self.prefix = prefix
        self.suffix = suffix
        self.bus_separator = bus_separator
        self.clk = clk
        self.reset = reset
        self.active_high_reset = active_high_reset
        self.uppercase = uppercase
        self.bus = self.get_main_link_bus()

    def get_main_link_bus(self) -> BusBaseClass:
        """Creates and returns the main link bus object for DisplayPort transmission.

        This bus object includes signals for main link data transmission, handling
        raw data from the frame generator, processed data with MSA, and final data
        from the `test_source` module.

        Returns:
            BusBaseClass: The main link bus object for DisplayPort.
        """
        signals = [  
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

        return BusBaseClass(dut=self.dut, name="", signals=signals, clk=self.clk, reset=self.reset)


"""AuxChannelBus."""
class AuxChannelBus:
    """AUX Channel Bus class for auxiliary channel management signals in DisplayPort."""

    def __init__(
        self,
        dut: cocotb.SimHandle,
        prefix: str = "",
        suffix: str = "",
        bus_separator: str = "_",
        clk: str = "clk",
        reset: str = "rst_n",
        active_high_reset: bool = True,
        uppercase: bool = False,
    ):
        """Constructor for AuxChannelBus.

        Args:
            dut (cocotb.SimHandle): Device under test handle to access signals.
            prefix (str): Prefix for signal names in the bus.
            suffix (str): Suffix for signal names in the bus.
            bus_separator (str): Separator used in signal naming.
            clk (str): Clock signal name.
            reset (str): Reset signal name.
            active_high_reset (bool): If True, reset is active high; otherwise, active low.
            uppercase (bool): If True, convert bus signal names to uppercase.
        """
        self.dut = dut
        self.prefix = prefix
        self.suffix = suffix
        self.bus_separator = bus_separator
        self.clk = clk
        self.reset = reset
        self.active_high_reset = active_high_reset
        self.uppercase = uppercase
        self.bus = self.get_aux_channel_bus()

    def get_aux_channel_bus(self) -> BusBaseClass:
        """Creates and returns the AUX channel bus object for DisplayPort auxiliary channel management.

        This bus object includes signals for AUX channel management, EDID, and DisplayPort capabilities.

        Returns:
            BusBaseClass: The AUX channel bus object for DisplayPort.
        """
        signals = [
            "debug" ,
            "hpd" ,
            "auxch_in" ,
            "auxch_out" ,
            "auxch_tri" ,        
            "stream_channel_count" ,
            "source_channel_count" ,
            "tx_clock_train" ,
            "tx_align_train" ,
            "tx_powerup_channel" ,
            "tx_preemp_0p0" ,
            "tx_preemp_3p5" ,
            "tx_preemp_6p0" ,           
            "tx_swing_0p4" ,
            "tx_swing_0p6" ,
            "tx_swing_0p8" ,          
            "tx_running" ,
            "tx_link_established" ,
            "auxch_data" ,
            "hotplug_detect"
        ]

        if self.uppercase:
            signals = [sig.upper() for sig in signals]
        signals = [f"{self.prefix}{self.bus_separator}{sig}{self.suffix}" for sig in signals]

        return BusBaseClass(dut=self.dut, name="", signals=signals, clk=self.clk, reset=self.reset)
