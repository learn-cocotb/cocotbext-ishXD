`timescale 1ns / 1ps

//////////////////////////////////////////////////////
// tb_dummy_sink_actual_tb.v 
//
// This is the proper wrapper code for dp_sink.v 
// tb_dummy_sink.v explicitly drives edid blocks 
// and other data but this does not.
//////////////////////////////////////////////////////


module tb_dummy_sink_actual_tb(
    input clk100,
    output auxch_data,
    output reg   hotplug_detect
    );

wire [7:0] sender_debug_pmod;
wire       sender_aux_tri;
 
reg        sender_wr_en;
reg [7:0]  sender_wr_data;
wire       sender_wr_full;
       //----------------------------                                  
reg        sender_rd_en;
wire [7:0] sender_rd_data;
wire       sender_rd_empty;
wire       sender_busy;
wire       sender_timeout;
reg        sender_abort;

aux_interface sender(
       .clk         (clk100),
       .debug_pmod  (sender_debug_pmod),
       //----------------------------
       .aux_in      (1'b1),
       .aux_out     (auxch_data),
       .aux_tri     (sender_aux_tri),
       //----------------------------
       .tx_wr_en    (sender_wr_en),
       .tx_data     (sender_wr_data),
       .tx_full     (sender_wr_full),
       //----------------------------                                  
       .rx_rd_en    (sender_rd_en),
       .rx_data     (sender_rd_data),
       .rx_empty    (sender_rd_empty),
       //----------------------------
       .busy        (sender_busy),
       .abort       (sender_abort),
       .timeout     (sender_timeout)
     );



initial begin
    $dumpfile("dp_sink.vcd");
	$dumpvars;

    hotplug_detect  = 1'b0;
    sender_wr_en    = 1'b0;
    sender_wr_data  = 8'h00;
    sender_rd_en    = 1'b0;
    sender_abort    = 1'b0;
    sender_rd_en = 1'b0;
    sender_wr_en = 1'b0;
    sender_abort = 1'b0;
    
    #1000
    hotplug_detect = 1'b1;
    
    #200000
    
    /////////////////////////////////////////////////////
    //  Reply to the read command
    //////////////////////////////////////////////////////
    sender_wr_data   = 8'h00;
    sender_wr_en  = 1'b1;
    #10
    sender_wr_en  = 1'b0;

    #300000

    sender_wr_en  = 1'b0;

    #200000000
    sender_wr_en  = 1'b0;

end     

endmodule