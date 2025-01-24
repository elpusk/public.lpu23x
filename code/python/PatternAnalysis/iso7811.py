
import bin_operation as bin_op

# global constants definition

# ISO 7811-2
CONST_INT_ISO2_START_BIT_POS_IN_BYTE = 3 #ISO2 문자를 MSb->LSB 로 우측정렬시 데이터가 시작되는 bit position 의 zero-base index(including parity bit)
CONST_INT_ISO2_SIZE_BIT = 5 # 5 bits(including parity bit)
CONST_BYTE_ISO2_ADD_FOR_ASC = 0x30

CONST_BYTE_ISO2_SS = 0x0B # Start Sentinel with parity(MSB), total 5 bits, right arrangement
CONST_BYTE_ISO2_ES = 0x1F # End Sentinel with parity(MSB), total 5 bits, right arrangement

CONST_ARRAY_BIN_ISO2_SS = [0, 1, 0, 1, 1] # Start Sentinel with parity(index 0 is MSB)
CONST_ARRAY_BIN_ISO2_ES = [1, 1, 1, 1, 1] # End Sentinel with parity(index 0 is MSB)
CONST_ARRAY_BIN_ISO2_SS_INV_ORDER = [1, 1, 0, 1, 0] # Start Sentinel with parity(index 4 is MSB)
CONST_ARRAY_BIN_ISO2_ES_INV_ORDER = [1, 1, 1, 1, 1] # End Sentinel with parity(index 4 is MSB)

CONST_INT_ISO2_MAX_SIZE_STR = 37 # ISO2 트랙에 저장 가능한 최대 문자수.(STX, ETX, LRC 제외)

CONST_STR_VAILD_ISO2_CHAR = "0123456789:;<=>?"
CONST_STR_VAILD_ISO2_CHAR_EXCEPT_SS_ES = "0123456789:<=>"

CONST_ARRAY_BIN_2D_TABLE_ISO2 = [[1, 0, 0, 0, 0], [0, 0, 0, 0, 1], [0, 0, 0, 1, 0], [1, 0, 0, 1, 1], [0, 0, 1, 0, 0], [1, 0, 1, 0, 1], [1, 0, 1, 1, 0], [0, 0, 1, 1, 1], [0, 1, 0, 0, 0], [1, 1, 0, 0, 1], [1, 1, 0, 1, 0], [0, 1, 0, 1, 1], [1, 1, 1, 0, 0], [0, 1, 1, 0, 1], [0, 1, 1, 1, 0], [1, 1, 1, 1, 1]]
def iso2_generate_char_table_without_parity():
    return bin_op.bin_generate_all_combination(CONST_INT_ISO2_SIZE_BIT - 1)

def iso2_generate_char_table_with_parity():
    char_table = iso2_generate_char_table_without_parity()
    return [bin_op.bin_add_parity(char, b_parity_msb=True, b_parity_odd=True) for char in char_table]

def iso2_generate_2d_bin_array_card_data(s_ascii_data):
    result = []
    if len(s_ascii_data) <=0:
        return result
    #
    for char in s_ascii_data:
        if char not in CONST_STR_VAILD_ISO2_CHAR_EXCEPT_SS_ES:
            return result #raise ValueError(f"문자 '{char}'는 허용되지 않는 문자입니다.")
    #
    ar_index = []
    c_lrc = CONST_BYTE_ISO2_SS

    for char in s_ascii_data:
        c = ord(char) - CONST_BYTE_ISO2_ADD_FOR_ASC
        ar_index.append(c)
        c_lrc = c_lrc ^ c # xor
        print(bin(c_lrc))
    #
    c_lrc = c_lrc ^ CONST_BYTE_ISO2_ES # xor
    ar_lrc = bin_op.bin_get_binary_array_from_byte(c_lrc,n_start=CONST_INT_ISO2_START_BIT_POS_IN_BYTE+1,n_bit_size=CONST_INT_ISO2_SIZE_BIT-1) # ignore parity bit
    ar_lrc = [bin_op.bin_calculate_parity(ar_lrc,b_parity_odd=True)]+ar_lrc
    
    result.append(CONST_ARRAY_BIN_ISO2_SS)
    for index in ar_index:
        ar = CONST_ARRAY_BIN_2D_TABLE_ISO2[index]
        result.append(ar)
    #
    result.append(CONST_ARRAY_BIN_ISO2_ES)
    result.append(ar_lrc)

    return result

'''
ar_1d_binary format - inversion order(STX),inversion order(D[0]), ... inversion order(D[N-1]), inversion order(ETX), inversion order(LRC)
return
Not detected STX : need_more_bits= True error_parity= False lrc_error= False data size= 0
dual detectd STX : need_more_bits= False error_parity= False lrc_error= False data size= 0
LRC is parity error : need_more_bits= False error_parity= True lrc_error= True data size>=0
Over lenght error : need_more_bits= False error_parity= False lrc_error= False data size>CONST_INT_ISO2_MAX_SIZE_STR
'''
def check_iso2_forward(ar_1d_binary):
    b_need_more_bits = True
    b_error_parity = False
    b_lrc_error = False
    n_the_number_of_chars_except_stx_etx_lrc = 0

    #
    if len(ar_1d_binary) < CONST_INT_ISO2_SIZE_BIT:
        return (b_need_more_bits,b_error_parity,b_lrc_error,n_the_number_of_chars_except_stx_etx_lrc)
    #
    ar_index_start_ss = bin_op.bin_find_pattern_in_1d_array(ar_1d_binary,CONST_ARRAY_BIN_ISO2_SS_INV_ORDER)
    if len(ar_index_start_ss) ==0 :
        # not found STX
        return (b_need_more_bits,b_error_parity,b_lrc_error,n_the_number_of_chars_except_stx_etx_lrc)
    #
    ar_2d_bin = bin_op.bin_get_2d_from_1d(ar_1d_binary,CONST_INT_ISO2_SIZE_BIT,ar_index_start_ss[0])
    #
    n_loop = len(ar_2d_bin)
    if len(ar_2d_bin[n_loop-1]) == CONST_INT_ISO2_SIZE_BIT:
        b_need_more_bits = False
    else:
        n_loop = n_loop - 1
    #
    b_detected_stx = False
    b_detected_etx = False
    b_detected_lrc = False
    c_cal_lrc = 0x00
    ba_cal_lrc = bytearray()
    ba_cc = bytearray()
    #
    for i in range(n_loop):
        if not b_detected_stx:
            if ar_2d_bin[i] == CONST_ARRAY_BIN_ISO2_SS_INV_ORDER:
                b_detected_stx = True
                cc = bin_op.bin_get_bytearray_from_binary_array(ar_2d_bin[i],0,CONST_INT_ISO2_SIZE_BIT,False)
                c_cal_lrc = cc[0]
                #
                ba_cc.append(cc[0])
                ba_cal_lrc.append(c_cal_lrc)
                #
            #
            continue
        # here detected STX
        if ar_2d_bin[i] == CONST_ARRAY_BIN_ISO2_SS_INV_ORDER:
            # dual STX - error
            b_error_parity = False
            b_lrc_error = False
            n_the_number_of_chars_except_stx_etx_lrc = 0
            b_need_more_bits = False
            return (b_need_more_bits,b_error_parity,b_lrc_error,n_the_number_of_chars_except_stx_etx_lrc)
        #
        if not bin_op.bin_check_parity(ar_2d_bin[i],0,CONST_INT_ISO2_SIZE_BIT,b_odd_parity=True):
            b_error_parity = True
            if b_detected_etx:
                b_lrc_error = True # parity error of LRC 
            break
        #
        if b_detected_etx:
            # LRC value
            clrc = bin_op.bin_get_bytearray_from_binary_array(ar_2d_bin[i],0,CONST_INT_ISO2_SIZE_BIT,False)
            c_found_lrc = clrc[0]
            c_found_lrc = c_found_lrc & 0x0F
            c_cal_lrc = c_cal_lrc & 0x0F
            #
            if c_found_lrc!=c_cal_lrc:
                b_lrc_error = True
            #
            b_detected_lrc = True
            break # exit for
        else:
            cc = bin_op.bin_get_bytearray_from_binary_array(ar_2d_bin[i],0,CONST_INT_ISO2_SIZE_BIT,False)
            c_cal_lrc = c_cal_lrc ^ cc[0]

            ba_cc.append(cc[0])
            ba_cal_lrc.append(c_cal_lrc)
        #
        if ar_2d_bin[i] == CONST_ARRAY_BIN_ISO2_ES_INV_ORDER:
            # detect inversion order ETX
            b_detected_etx = True
        else:
            n_the_number_of_chars_except_stx_etx_lrc = n_the_number_of_chars_except_stx_etx_lrc + 1
        #
    # end for

    while not b_need_more_bits:
        if not b_detected_stx:
            b_need_more_bits = True
            break # end while
        # detected single STX.

        if b_error_parity:
            break # end while

        # none parity error
        if not b_detected_etx:
            b_need_more_bits = True
            break # end while

        # detected ETX
        if not b_detected_lrc:
            b_need_more_bits = True
            break # end while
        # detected LRC
        break
    # end while
    if b_need_more_bits:
        if n_the_number_of_chars_except_stx_etx_lrc > CONST_INT_ISO2_MAX_SIZE_STR:
            b_need_more_bits = False
    #
    return (b_need_more_bits,b_error_parity,b_lrc_error,n_the_number_of_chars_except_stx_etx_lrc)
#

def check_iso2_forward_with_2d(ar_bin_2d):
    ar_2d_normal = []
    b_continue = True
    #
    for ar_1d in ar_bin_2d:
        b_more,b_ep,b_el,n = check_iso2_forward(ar_1d)
        if b_more:
            ar_2d_normal.append(ar_1d)
        elif (not b_ep) and (not b_el):
            if n==0:
                # print(f"STX 두번 검출 : 데이터 길이는 {n} : {ar_1d_etx_d36_35}")
                continue
            else:
                # STX, ETX, LRC 찾음.
                # print(f"STX, ETX, LRC 모두 만족 : 데이터 길이는 {n} : {ar_1d}")
                # print(f"따라서 명제는 거짓")
                b_continue = False
                break
            #
        elif b_ep and b_el:
            # print(f"LRC의 parity 에러 : 데이터 길이는 {n} :{ar_1d}")
            continue
        elif b_ep:
            # print(f"parity 에러 : 데이터 길이는 {n} : {ar_1d}")
            continue
        else:
            # print(f"LRC 에러 : 데이터 길이는 {n} :{ar_1d}")
            continue
    # and for
    return (b_continue,ar_2d_normal)
# 