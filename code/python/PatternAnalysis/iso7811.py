
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
    ar_lrc = bin_op.bin_byte_to_binary_array(c_lrc,n_start=CONST_INT_ISO2_START_BIT_POS_IN_BYTE+1,n_bit_size=CONST_INT_ISO2_SIZE_BIT-1) # ignore parity bit
    ar_lrc = [bin_op.bin_calculate_parity(ar_lrc,b_parity_odd=True)]+ar_lrc
    
    result.append(CONST_ARRAY_BIN_ISO2_SS)
    for index in ar_index:
        ar = CONST_ARRAY_BIN_2D_TABLE_ISO2[index]
        result.append(ar)
    #
    result.append(CONST_ARRAY_BIN_ISO2_ES)
    result.append(ar_lrc)

    return result