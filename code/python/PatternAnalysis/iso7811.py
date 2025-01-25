
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

'''
@brief 
    패리티 비트를 제외한 4 비트가 생성 가능한 모든 조합의 이차원 이진 배열 생성.
@param
    none
@return
    생성된 2^4 by 4 이차원 배열
'''
def iso2_generate_char_table_without_parity():
    return bin_op.bin_generate_all_combination(CONST_INT_ISO2_SIZE_BIT - 1)

'''
@brief 
    패리티 비트를 제외한 4 비트가 생성 가능한 모든 조합의 이차원 이진 배열 생성하고,
    생성된 2차원 이진 배열의 각 행의 시작에 각 행의 odd parity 비트 값을 추가. 
@param
    none
@return
    생성된 2^4 by 5 이차원 배열
'''
def iso2_generate_char_table_with_parity():
    char_table = iso2_generate_char_table_without_parity()
    return [bin_op.bin_add_parity(char, b_parity_msb=True, b_parity_odd=True) for char in char_table]

'''
@brief 
    아스키 코드로 구성된 문자열 s_ascii_data 의 각 문자에 대응하는 ISO7811-2 track2 코드값을 1차원 이진배열로 하는 이차원 이진배열 생성.
    STX, ETC, LRC 는 자동으로 추가 된다.  
@param
    s_ascii_data - 아스키 코드로 구성된 문자열
@return
    생성된 이차원 이진배열
'''
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
@brief 
    ar_1d_binary 로 주어지는 1차원 이진 배열이 ISO7811-2 track 2를 forward 로 읽었을 때, 얻는 값이라고 가정하고, 규격에 맞는지 검사.
    ar_1d_binary format - inversion order(STX),inversion order(D[0]), ... inversion order(D[N-1]), inversion order(ETX), inversion order(LRC)
@param
    ar_1d_binary - ISO7811-2 track 2를 forward 로 읽었을 때, 얻는 1차원 이진 배열
@return
    need_more_bits - True 면, ar_1d_binary 로 주어진 값까지에서는 에러가 발견되지 않았거나, STX 가 발견되지 않았거나, 데이터의 마지막을 구성하는 LRC 값 까지 받지 못함.
                   - False, LRC 까지 주어진 데이터 상에 에러가 발생 또는 리살   
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

'''
@brief 
    invert all bits of the given binary array.
@param
    array_bin - 1d binary array
@return
    binary array
'''
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