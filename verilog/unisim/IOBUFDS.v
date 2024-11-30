module IOBUFDS #(
    parameter DIFF_TERM = "FALSE",     // Differential termination
    parameter IBUF_LOW_PWR = "TRUE",   // Low power option
    parameter IOSTANDARD = "DEFAULT",  // I/O standard
    parameter SLEW = "SLOW"            // Output slew rate
)(
    output O,      // Buffer output
    inout IO,      // Diff_p inout (positive)
    inout IOB,     // Diff_n inout (negative)
    input I,       // Buffer input
    input T        // 3-state control input
);

    // Internal signals for IO and IOB when T is active
    reg io_reg;
    reg iob_reg;
    
    // Drive IO and IOB based on the input I and tristate T
    assign IO  = T ? 1'bz : io_reg;     // High impedance if T is high
    assign IOB = T ? 1'bz : iob_reg;    // High impedance if T is high

    // Drive output O based on the differential inputs IO and IOB
    assign O = (IO == ~IOB) ? IO : 1'bx; // X if mismatch for simple simulation

    // Logic to handle I/O buffering
    always @(*) begin
        if (T == 1'b0) begin
            io_reg  = I;     // IO matches I
            iob_reg = ~I;    // IOB matches inverted I
        end else begin
            io_reg  = 1'bz;  // High impedance for both IO
            iob_reg = 1'bz;  // and IOB when T is high
        end
    end

endmodule
