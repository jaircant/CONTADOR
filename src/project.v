module tt_nm_contador_3bits (
    input  wire       CLK,
    input  wire       RESET_N,
    input  wire       PAUSA,
    output reg  [2:0] CUENTA
);

    always @(posedge CLK or negedge RESET_N) begin
        if (!RESET_N)
            CUENTA <= 3'b000;
        else if (!PAUSA)
            CUENTA <= CUENTA + 3'd1;
    end

endmodule


module tt_um_contador_3bits (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

    wire [2:0] cuenta;

    tt_nm_contador_3bits contador (
        .CLK     (clk),
        .RESET_N (rst_n),
        .PAUSA   (ui_in[7] || !ena),
        .CUENTA  (cuenta)
    );

    assign uo_out  = {5'b00000, cuenta};
    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;

endmodule
