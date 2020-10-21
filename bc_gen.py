# Frustrated
def main(file_handler):
    # file header
    file_handler.write("BC1.1\n")

    """
    carry lookahead 32 bit adder
    
    P0_0 := NOT(NOT(OR(A0,B0)));
    G0_0 := NOT(NOT(AND(A0,B0)));
    S_lookahead_0 := ODD(A0,B0,C_lookahead_0);
    
    ...
    
    P0_31 := NOT(NOT(OR(A31,B31)));
    G0_31 := NOT(NOT(AND(A31,B31)));
    S_lookahead_31 := ODD(A31,B31,C_lookahead_31);
    
    P1_0 := NOT(NOT(AND(P0_0,P0_1)));
    G1_0 := NOT(AND(NOT(G0_1),NOT(AND(G0_0,P0_1))));
    C_lookahead_1 := NOT(AND(NOT(G0_0), NOT(AND(P0_0,C_lookahead_0))));
    
    ...
    
    P1_15 := NOT(NOT(AND(P0_30,P0_31)));
    G1_15 := NOT(AND(NOT(G0_31),NOT(AND(G0_30,P0_31))));
    C_lookahead_31 := NOT(AND(NOT(G0_30), NOT(AND(P0_30,C_lookahead_30))));
    
    ...
    
    P2_0 := NOT(NOT(AND(P1_0,P1_1)));
    G2_0 := NOT(AND(NOT(G1_1),NOT(AND(G1_0,P1_1))));
    C_lookahead_2 := NOT(AND(NOT(G1_0), NOT(AND(P1_0, C_lookahead_0))));
    
    ...
    
    P2_7 := NOT(NOT(AND(P1_14,P1_15)));
    G2_7 := NOT(AND(NOT(G1_15),NOT(AND(G1_14,P1_15))));
    C_lookahead_30 := NOT(AND(NOT(G1_14), NOT(AND(P1_14, C_lookahead_28))));
    
    P3_0 := NOT(NOT(AND(P2_0,P2_1)));
    G3_0 := NOT(AND(NOT(G2_1),NOT(AND(G2_0,P2_1))));
    C_lookahead_4 := NOT(AND(NOT(G2_0), NOT(AND(P2_0, C_lookahead_0))));
    
    ...
    
    P3_3 := NOT(NOT(AND(P2_6,P2_7)));
    G3_3 := NOT(AND(NOT(G2_7),NOT(AND(G2_6,P2_7))));
    C_lookahead_28 := NOT(AND(NOT(G2_6), NOT(AND(P2_6, C_lookahead_24))));
    
    ...
    
    P4_0 := NOT(NOT(AND(P3_0,P3_1)));
    G4_0 := NOT(AND(NOT(G3_1),NOT(AND(G3_0,P3_1))));
    C_lookahead_8 := NOT(AND(NOT(G3_0), NOT(AND(P3_0, C_lookahead_0))));
    
    P4_1 := NOT(NOT(AND(P3_2,P3_3)));
    G4_1 := NOT(AND(NOT(G3_3),NOT(AND(G3_2,P3_3))));
    C_lookahead_24 := NOT(AND(NOT(G3_2), NOT(AND(P3_2, C_lookahead_16))));
    
    P5_0 := NOT(NOT(AND(P4_0,P4_1)));
    G5_0 := NOT(AND(NOT(G4_1),NOT(AND(G4_0,P4_1))));
    C_lookahead_16 := NOT(AND(NOT(G4_0), NOT(AND(P4_0,ALUFN0))));
    """

    count = 32
    index = 0
    while count:
        if count == 32:
            for boxA in range(count):
                px_x = "P{0}_{1} := NOT(NOT(OR(A{1},B{1})));\n".format(index, boxA)
                gx_x = "G{0}_{1} := NOT(NOT(AND(A{1},B{1})));\n".format(index, boxA)
                new_sx = "S_lookahead_{0} := ODD(A{0},B{0},C_lookahead_{0});\n".format(boxA)
                file_handler.write(px_x)
                file_handler.write(gx_x)
                file_handler.write(new_sx)
                file_handler.write('\n')
        else:
            for boxB in range(count):
                px_x = 'P{0}_{2} := NOT(NOT(AND(P{1}_{3},P{1}_{4})));\n'.format(index, index - 1, boxB, boxB * 2,
                                                                               boxB * 2 + 1)
                gx_x = 'G{0}_{2} := NOT(AND(NOT(G{1}_{4}),NOT(AND(G{1}_{3},P{1}_{4}))));\n'.format(index, index - 1, boxB,
                                                                                                boxB * 2,
                                                                                                boxB * 2 + 1)
                new_coutx = 'C_lookahead_{2} := NOT(AND(NOT(G{0}_{3}), NOT(AND(P{0}_{3},C_lookahead_{1}))));\n'.format(
                    index - 1, boxB * (2 ** index), boxB * (2 ** index) + (2 ** (index - 1)), boxB * 2)
                file_handler.write(px_x)
                file_handler.write(gx_x)
                file_handler.write(new_coutx)
                file_handler.write('\n')
        count //= 2
        index += 1

    file_handler.write('C_lookahead_0 := (ALUFN0);\n')
    file_handler.write('Z := ODD(S31, S_lookahead_31);\n')
    file_handler.write('ASSIGN Z;')

    """
        Ripple Carry 32 bit adder

        bit1
        B0 := ODD(b0,ALUFN0);
        S0 := ODD(A0,B0,ALUFN0);
        C0 := OR(AND(A0,B0),AND(ALUFN0,A0),AND(ALUFN0,B0));

        bit2
        B1 := ODD(b1,ALUFN0);
        S1 := ODD(A1,B1,C0);
        C1 := OR(AND(A1,B1),AND(C0,A1),AND(C0,A1));

        bit3
        B2 := ODD(b2,ALUFN0);
        S2 := ODD(A2,B2,C0);
        C2 := OR(AND(A2,B2),AND(C1,A2),AND(C1,A2));

        ...

        bit 32
        B31 := ODD(b31,ALUFN0);
        S31 := ODD(A31,B31,C0);
        C31 := OR(AND(A2,B2),AND(C1,A2),AND(C1,A2));
        """

    # the first bit
    file_handler.write('B0 := ODD(b0,ALUFN0);\n')
    file_handler.write('S0 := ODD(A0,B0,ALUFN0);\n')
    file_handler.write('C1 := OR(AND(A0,B0),AND(ALUFN0,A0),AND(ALUFN0,B0));\n')
    file_handler.write('\n')

    for i in range(1, 32):
        bx = "B{0} := ODD(b{0},ALUFN0);\n".format(i)
        sx = "S{0} := ODD(A{0},B{0},C{1});\n".format(i, i)
        coutx = "C{1} := OR(AND(A{0},B{0}),AND(C{0},A{0}),AND(C{0},B{0}));\n".format(i, i + 1)
        file_handler.write(bx + sx + coutx + '\n')

    print("done")


if __name__ == "__main__":
    bs = open("adder32bit.bc", "w")
    main(bs)
    bs.close()
