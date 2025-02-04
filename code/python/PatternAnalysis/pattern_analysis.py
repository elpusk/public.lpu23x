
import bin_operation as bin_op
import iso7811 as iso
import pandas as pd
import numpy as np
import time
import numba

#
# @jit(nopython=True)
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
    # print(found_index)
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
    

    print("forward 읽기로 검사하여, 모든 조건을 에러 없이 만족하거나, 에러가 나는 조합은 제거")

    b_continue = False

    ad_bin_2d_in = found_2d_etx_d36
    ad_bin_2d_out = []
    n_last_index = -1 # 35~0
    # n_last_index = 31 # 35~34

    for d in range(35,n_last_index-1,-1):
        # D[35] ~ D[0] session
        start_time = time.time()
        print(f"===== D[{d}] session")
        #
        ad_bin_2d_out = [] # reset out array
        # 
        for _1d in ad_bin_2d_in:
            _2d = bin_op.bin_concate_1D_bin_to_2d_bin(_1d,ar_2d_all_except_ETX,True)
            # print(_1d)
            # bin_op.bin_print_2d(_2d)
            b_continue, normal_2d = iso.check_iso2_forward_with_2d(_2d)
            if not b_continue:
                end_time = time.time()
                print("Elapsed Time : ",end_time-start_time)
                print(f"STX, ETX, LRC 모두 만족하고, 데이터의 길이가 0보다 큰 조합 발견.따라서 명제는 거짓")
                return
            #
            ad_bin_2d_out = bin_op.bin_concate_2d_bin_to_2d_bin(ad_bin_2d_out,normal_2d) 
        # end for _1d
        # bin_op.bin_print_2d(ad_bin_2d_out,"-")
        print( f"ETX, D[36] ~ D[{d}] 까지 명제를 참으로 유지하는 조합의 수는 ",len(ad_bin_2d_out))

        ad_bin_2d_in = ad_bin_2d_out
        end_time = time.time()
        print("Elapsed Time : ",end_time-start_time)

    #end for range(35,-1,-1)

    print("가능한 모든 조합에서 위 명제에 반하는 경우가 없으므로, 명제는 참.")
#

if __name__ == "__main__":
    main()
