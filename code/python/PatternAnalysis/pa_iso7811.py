
import pa_bin_operation as bin_op
import itertools
import pyarrow as pa

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
    패리티 비트를 제외한 4 비트가 생성 가능한 모든 조합의 pyArrow 2차원 배열 생성.
@param
    none
@return
    생성된 2^4 by 4 pyArrow 2차원 배열
'''
def iso2_generate_char_table_without_parity():
    return bin_op.bin_generate_all_combination(CONST_INT_ISO2_SIZE_BIT - 1)

'''
@brief 
    패리티 비트를 제외한 4 비트가 생성 가능한 모든 조합의 pyArrow 2차원 배열 생성하고,
    생성된 pyArrow 2차원 배열의 각 행의 시작에 각 행의 odd parity 비트 값을 추가. 
@param
    none
@return
    생성된 2^4 x 5 pyArrow 2차원 배열
'''
def iso2_generate_char_table_with_parity()->pa.ListArray:
    """
    Generate a 2D PyArrow array with all possible 4-bit combinations,
    and prepend each row with an odd parity bit.

    Returns:
        pa.Table: A 16x5 PyArrow 2D binary array.
    """
    # Generate all 4-bit combinations (2^4 = 16)
    bit_combinations = list(itertools.product([0, 1], repeat=4))
    
    # Compute odd parity and prepend to each row
    data_with_parity = [
        [1 if sum(bits) % 2 == 0 else 0] + list(bits)  # Odd parity bit (MSB)
        for bits in bit_combinations
    ]

    # Convert to PyArrow 2D array
    arrow_array = pa.array(data_with_parity)

    return arrow_array

'''
@brief 
    아스키 코드로 구성된 문자열 s_ascii_data 의 각 문자에 대응하는 ISO7811-2 track2 코드값을 pyArrow 1차원 배열로 하는 pyArrow 2차원 배열 생성.
    STX, ETC, LRC 는 자동으로 추가 된다.  
@param
    s_ascii_data - 아스키 코드로 구성된 문자열
@return
    생성된 pyArrow 2차원 배열 
'''
def iso2_generate_2d_bin_array_card_data(s_ascii_data:str)->pa.ListArray:
    """
    Generate a 2D PyArrow binary array representing an ISO7811-2 Track 2 encoded card data.

    The function:
    - Converts ASCII characters to their corresponding 4-bit ISO7811-2 representations.
    - Adds STX (Start Sentinel), ETX (End Sentinel), and LRC (Longitudinal Redundancy Check).
    - Converts the final bitstream into a 2D PyArrow binary array.

    Parameters:
        s_ascii_data (str): The ASCII string to be encoded.

    Returns:
        pa.Table: A PyArrow 2D binary array representing the encoded Track 2 data.
    """

    # ISO7811-2 Track 2 encoding table (4-bit BCD encoding)
    iso2_table = {
        '0': [0, 0, 0, 0], '1': [0, 0, 0, 1], '2': [0, 0, 1, 0], '3': [0, 0, 1, 1],
        '4': [0, 1, 0, 0], '5': [0, 1, 0, 1], '6': [0, 1, 1, 0], '7': [0, 1, 1, 1],
        '8': [1, 0, 0, 0], '9': [1, 0, 0, 1], ':': [1, 0, 1, 0], ';': [1, 0, 1, 1],  # ';' = Start Sentinel
        '<': [1, 1, 0, 0], '=': [1, 1, 0, 1], '>': [1, 1, 1, 0], '?': [1, 1, 1, 1]  # '?' = End Sentinel
    }

    # Track 2 specific characters
    STX = [1, 0, 1, 1]  # Start Sentinel ';'
    ETX = [1, 1, 1, 1]  # End Sentinel '?'

    # Convert ASCII data to binary using the table
    bin_data = [iso2_table[char] for char in s_ascii_data if char in iso2_table]

    # Add STX at the beginning and ETX at the end
    bin_data.insert(0, STX)
    bin_data.append(ETX)

    # Compute LRC (Longitudinal Redundancy Check)
    lrc = [0, 0, 0, 0]
    for bits in bin_data:
        lrc = [lrc[i] ^ bits[i] for i in range(4)]
    bin_data.append(lrc)

    # Convert to PyArrow 2D array
    arrow_array = pa.array(bin_data)

    return arrow_array

'''
@brief 
    ar_1d_binary 로 주어지는 PyArrow 1차원 배열이 ISO7811-2 track 2를 forward 로 읽었을 때, 얻는 값이라고 가정하고, 규격에 맞는지 검사.
    forward 로 읽었을 때, 얻는 값 형식은 - inversion order(STX),inversion order(D[0]), ... inversion order(D[N-1]), inversion order(ETX), inversion order(LRC)
@param
    ar_1d_binary - ISO7811-2 track 2를 forward 로 읽었을 때, 얻는 PyArrow 1차원 배열
@return
    need_more_bits - True 면, ar_1d_binary 로 주어진 값까지에서는 에러가 발견되지 않았거나, STX 가 발견되지 않았거나, 데이터의 마지막을 구성하는 LRC 값 까지 받지 못함.
                   - False, LRC 까지 주어진 데이터 상에 에러가 발생 또는 리살   
    Not detected STX : need_more_bits= True error_parity= False lrc_error= False data size= 0
    dual detectd STX : need_more_bits= False error_parity= False lrc_error= False data size= 0
    LRC is parity error : need_more_bits= False error_parity= True lrc_error= True data size>=0
    Over lenght error : need_more_bits= False error_parity= False lrc_error= False data size>CONST_INT_ISO2_MAX_SIZE_STR
'''
def check_iso2_forward(ar_1d_binary:pa.array):
    b_need_more_bits = True
    b_error_parity = False
    b_lrc_error = False
    n_the_number_of_chars_except_stx_etx_lrc = 0

    # Ensure input arrays are of type pyarrow.Array
    if not isinstance(ar_1d_binary, pa.Array):
        raise TypeError("Both array_bin and pattern must be pyarrow arrays.")
    #
    if ar_1d_binary.length() < CONST_INT_ISO2_SIZE_BIT:
        return (b_need_more_bits,b_error_parity,b_lrc_error,n_the_number_of_chars_except_stx_etx_lrc)
    #
    ar_index_start_ss = bin_op.bin_find_pattern_in_1d_array(ar_1d_binary,CONST_ARRAY_BIN_ISO2_SS_INV_ORDER)
    if ar_index_start_ss.length() ==0 :
        # not found STX
        return (b_need_more_bits,b_error_parity,b_lrc_error,n_the_number_of_chars_except_stx_etx_lrc)
    #
    ar_2d_bin = bin_op.bin_get_2d_from_1d(ar_1d_binary,CONST_INT_ISO2_SIZE_BIT,ar_index_start_ss[0])
    #
    n_loop = ar_2d_bin.length()
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
def check_iso2_forward_with_2d(ar_bin_2d:pa.ListArray):
    ar_2d_normal = pa.array([])
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