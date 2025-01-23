
import bin_operation as bin_op
import iso7811 as iso
import pandas as pd
import numpy as np

#
def main():
    print("ETX  = inv(ETX) 이므로, ETX 를 inv(ETX) 로 인식하는 경우")
    print("LRC = inv(STX) 이고 D[N-1] = 00100 이다")
    print("정방향으로 해석하면, ETX 전에 문자가 1개만 있으므로 그 문자(LRC)는 inv(STX)와 같아야 한다. 따라서")
    print("LRC = inv(STX) 이고 D[N-1] = 00100 이어야 한다.")
    #
    print("나올수  있는 모든 LRC 조합(16개) 과 ETX 를 연결해보면,")

    # 5 비트로 구성된 모든 조합. 생성
    ar_2d_all_without_parity = bin_op.bin_generate_all_combination(4);
    ar_2d_all = bin_op.bin_add_parity(ar_2d_all_without_parity,b_parity_msb=True,b_parity_odd=True)

    # 모든 조합에서 ISO2 STX inversion order(CONST_ARRAY_BIN_ISO2_SS_INV_ORDER) 만 제거. 
    ar_2d_all_lrc = bin_op.bin_remove_matching_rows(ar_2d_all,iso.CONST_ARRAY_BIN_ISO2_SS_INV_ORDER)

    # 모든 조합의 뒤에 ISO2 ETX (CONST_ARRAY_BIN_ISO2_ES)를 추가.
    ar_2d_all_lrc_etx = bin_op.bin_concate_1D_bin_to_2d_bin(iso.CONST_ARRAY_BIN_ISO2_ES,ar_2d_all_lrc,False)
    #print(pd.DataFrame(ar_2d_all_lrc_etx))

    # 모든 조합에서 CONST_ARRAY_BIN_ISO2_SS_INV_ORDER 가 있는 지 검사. 
    found_index = bin_op.bin_find_pattern_in_2d_array(ar_2d_all_lrc_etx,iso.CONST_ARRAY_BIN_ISO2_SS_INV_ORDER)
    #print(found)
    if bin_op.bin_is_empty_2d_binary_array(found_index) is not True:
        # print("LRC-ETX : inv_order(stx) : not empty")
        print("Inv(STX-11010)는 LRC, ETX 에 걸쳐 나올 수 있다.")
        print("따라서 == 명제는 거짓. ==")
        return
    # not found here
    print("Inv(STX-11010)는 LRC, ETX 에 걸쳐 나올 수 없다.")

    ## ETX, D[36]
    # 모든 조합에서 STX, ETX 제거
    ar_2d_all_except_ETX = bin_op.bin_remove_matching_rows(ar_2d_all,iso.CONST_ARRAY_BIN_ISO2_ES)
    ar_2d_all_except_STX_ETX = bin_op.bin_remove_matching_rows(ar_2d_all_except_ETX,iso.CONST_ARRAY_BIN_ISO2_SS)

    # 모든 조합의 앞에 ISO2 ETX (CONST_ARRAY_BIN_ISO2_ES)를 추가.
    ar_2d_etx_all = bin_op.bin_concate_1D_bin_to_2d_bin(iso.CONST_ARRAY_BIN_ISO2_ES,ar_2d_all_except_ETX,True)

    # 모든 조합에서 CONST_ARRAY_BIN_ISO2_SS_INV_ORDER 가 있는 지 검사. 
    found_index = bin_op.bin_find_pattern_in_2d_array(ar_2d_etx_all,iso.CONST_ARRAY_BIN_ISO2_SS_INV_ORDER)
    print(found_index)
    if bin_op.bin_is_empty_2d_binary_array(found_index) is True:
        # not found here
        # print("ETX-D[36] : inv_order(stx) : empty")
        print("Inv(STX-11010)는 ETX,D[36] 에 걸쳐 나올 수 없다.")
        print("따라서 == 명제는 참. ==")
        return
    
    # found inversion order STX - 일단 STX 를 찾았음으로 아래 조합서는 d0 부터 추가
    found_2d_etx_d36 = bin_op.bin_get_2d_found_pattern(ar_2d_etx_all,iso.CONST_ARRAY_BIN_ISO2_SS_INV_ORDER)
    # bin_op.bin_print_2d(found_2d_etx_d36,"-")

    print("Inv(STX-11010)가 ETX,D[36] 에 걸쳐 나오는 경우. ")
    ar_2d_etx_d36_35_normal = []

    for etx_d36_1d in found_2d_etx_d36:
        # 가능한 모든 D[35] 조합의 앞에 검출된 ETX, D[36]를 추가.
        ar_2d_etx_d36_35 = bin_op.bin_concate_1D_bin_to_2d_bin(etx_d36_1d,ar_2d_all_except_ETX,True)
        # print(etx_d36_1d)
        # bin_op.bin_print_2d(ar_2d_etx_d36_35)
        for ar_1d_etx_d36_35 in ar_2d_etx_d36_35:
            if bin_op.bin_check_parity(ar_1d_etx_d36_35,iso.CONST_INT_ISO2_SIZE_BIT,iso.CONST_INT_ISO2_SIZE_BIT,b_odd_parity=True):
                ar_2d_etx_d36_35_normal.append(ar_1d_etx_d36_35)
        #
    #
    bin_op.bin_print_2d(ar_2d_etx_d36_35_normal,"-")


    '''

    # next
    ar_2d_all_data = ar_2d_all;
    ar_2d_etx_all_data = bin_op.bin_concate_1D_bin_to_2d_bin(iso.CONST_ARRAY_BIN_ISO2_ES,ar_2d_all_data,True)
    print(pd.DataFrame(ar_2d_etx_all_data))
    '''
#

if __name__ == "__main__":
    main()
