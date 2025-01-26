import numpy as np
import np_bin_operation as bin_op

# global constants definition

# ISO 7811-2
CONST_INT_ISO2_START_BIT_POS_IN_BYTE = 3 # ISO2 문자의 MSb->LSB 우측 정렬 시 데이터 시작 bit position (0-base index, 포함 parity bit)
CONST_INT_ISO2_SIZE_BIT = 5 # 5 bits (including parity bit)
CONST_BYTE_ISO2_ADD_FOR_ASC = 0x30

CONST_BYTE_ISO2_SS = 0x0B # Start Sentinel with parity (MSB), total 5 bits
CONST_BYTE_ISO2_ES = 0x1F # End Sentinel with parity (MSB), total 5 bits

CONST_ARRAY_BIN_ISO2_SS = np.array([0, 1, 0, 1, 1], dtype=np.uint8) # Start Sentinel with parity
CONST_ARRAY_BIN_ISO2_ES = np.array([1, 1, 1, 1, 1], dtype=np.uint8) # End Sentinel with parity
CONST_ARRAY_BIN_ISO2_SS_INV_ORDER = np.array([1, 1, 0, 1, 0], dtype=np.uint8) # Start Sentinel inverted
CONST_ARRAY_BIN_ISO2_ES_INV_ORDER = np.array([1, 1, 1, 1, 1], dtype=np.uint8) # End Sentinel inverted

CONST_INT_ISO2_MAX_SIZE_STR = 37 # ISO2 track 최대 문자 수 (STX, ETX, LRC 제외)

CONST_STR_VALID_ISO2_CHAR = "0123456789:;<=>?"
CONST_STR_VALID_ISO2_CHAR_EXCEPT_SS_ES = "0123456789:<=>"

CONST_ARRAY_BIN_2D_TABLE_ISO2 = np.array([
    [1, 0, 0, 0, 0], [0, 0, 0, 0, 1], [0, 0, 0, 1, 0], [1, 0, 0, 1, 1],
    [0, 0, 1, 0, 0], [1, 0, 1, 0, 1], [1, 0, 1, 1, 0], [0, 0, 1, 1, 1],
    [0, 1, 0, 0, 0], [1, 1, 0, 0, 1], [1, 1, 0, 1, 0], [0, 1, 0, 1, 1],
    [1, 1, 1, 0, 0], [0, 1, 1, 0, 1], [0, 1, 1, 1, 0], [1, 1, 1, 1, 1]
], dtype=np.uint8)

# Functions

def iso2_generate_char_table_without_parity():
    """
    패리티 비트를 제외한 4 비트가 생성 가능한 모든 조합의 이차원 이진 배열 생성
    """
    return bin_op.bin_generate_all_combination(CONST_INT_ISO2_SIZE_BIT - 1)

def iso2_generate_char_table_with_parity():
    """
    패리티 비트를 제외한 4 비트 배열에 odd parity 비트를 추가하여 반환
    """
    char_table = iso2_generate_char_table_without_parity()
    return np.array([
        bin_op.bin_add_parity(char, b_parity_msb=True, b_parity_odd=True)
        for char in char_table
    ])

def iso2_generate_2d_bin_array_card_data(s_ascii_data):
    """
    아스키 문자열을 ISO7811-2 형식으로 변환하여 이차원 이진 배열 생성
    """
    if not s_ascii_data or any(char not in CONST_STR_VALID_ISO2_CHAR_EXCEPT_SS_ES for char in s_ascii_data):
        return np.array([])

    result = np.array([CONST_ARRAY_BIN_ISO2_SS])
    c_lrc = CONST_BYTE_ISO2_SS
    ar_index = np.array([ord(char) - CONST_BYTE_ISO2_ADD_FOR_ASC for char in s_ascii_data], dtype=np.uint8)

    for c in ar_index:
        c_lrc ^= c
        np.append(result,CONST_ARRAY_BIN_2D_TABLE_ISO2[c])

    c_lrc ^= CONST_BYTE_ISO2_ES
    ar_lrc = bin_op.bin_get_binary_array_from_byte(
        c_lrc, n_start=CONST_INT_ISO2_START_BIT_POS_IN_BYTE + 1, n_bit_size=CONST_INT_ISO2_SIZE_BIT - 1
    )
    ar_lrc = np.insert(ar_lrc, 0, bin_op.bin_calculate_parity(ar_lrc, b_parity_odd=True))

    np.append(result,CONST_ARRAY_BIN_ISO2_ES)
    np.append(result,ar_lrc)

    return np.array(result, dtype=np.uint8)

def check_iso2_forward(ar_1d_binary):
    """
    ISO7811-2 track 2 형식 데이터의 유효성을 검사
    """
    if len(ar_1d_binary) < CONST_INT_ISO2_SIZE_BIT:
        return True, False, False, 0

    ar_index_start_ss = bin_op.bin_find_pattern_in_1d_array(ar_1d_binary, CONST_ARRAY_BIN_ISO2_SS_INV_ORDER)
    if len(ar_index_start_ss) == 0:
        return True, False, False, 0

    ar_2d_bin = bin_op.bin_get_2d_from_1d(
        ar_1d_binary, CONST_INT_ISO2_SIZE_BIT, ar_index_start_ss[0]
    )

    b_detected_stx, b_detected_etx, b_detected_lrc = False, False, False
    c_cal_lrc, n_chars = 0x00, 0

    for row in ar_2d_bin:
        if not b_detected_stx:
            if np.array_equal(row, CONST_ARRAY_BIN_ISO2_SS_INV_ORDER):
                b_detected_stx = True
                c_cal_lrc = bin_op.bin_get_byte_from_binary_array(row)
                continue
            continue

        if np.array_equal(row, CONST_ARRAY_BIN_ISO2_SS_INV_ORDER):
            return False, False, False, 0

        if not bin_op.bin_check_parity(row, 0, CONST_INT_ISO2_SIZE_BIT, b_odd_parity=True):
            return False, True, b_detected_etx, n_chars

        if b_detected_etx:
            c_found_lrc = bin_op.bin_get_byte_from_binary_array(row) & 0x0F
            if c_found_lrc != (c_cal_lrc & 0x0F):
                return False, True, True, n_chars
            b_detected_lrc = True
            break

        c_cal_lrc ^= bin_op.bin_get_byte_from_binary_array(row)
        n_chars += 1

        if np.array_equal(row, CONST_ARRAY_BIN_ISO2_ES_INV_ORDER):
            b_detected_etx = True

    if n_chars > CONST_INT_ISO2_MAX_SIZE_STR:
        return False, False, False, n_chars

    return not b_detected_lrc, False, False, n_chars

def check_iso2_forward_with_2d(ar_bin_2d):
    result = np.array([])
    for row in ar_bin_2d:
        b_more, b_ep, b_el, n = check_iso2_forward(row)
        if b_more:
            np.append(result,row)
        elif b_ep or b_el or n == 0:
            continue
        else:
            return False, np.array(result)
    return True, np.array(result)
