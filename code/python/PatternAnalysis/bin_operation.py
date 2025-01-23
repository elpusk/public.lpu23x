import pandas as pd

# binary arrary operations module

from itertools import product

# invert all bits of the given binary array.
def bin_invert_bits(array_bin):
    """Invert the bits of the given value based on n_bits."""
    return [1 - bit for bit in array_bin]

# invert the order of the given binary array.
def bin_invert_order(array_bin):
    """Invert the order of the given value based on n_bits."""
    return array_bin[::-1]

# invert the order of the given binary array.
# invert all bits of the given binary array.
def bin_invert_order_and_bits(array_bin):
    """Invert the order of the given value based on n_bits."""
    return [1 - bit for bit in array_bin][::-1]

# find pattern in the given binary array.
# return the index of the pattern in the array.
def bin_find_pattern_in_1d_array(array_bin, pattern):
    pattern_length = len(pattern)
    array_length = len(array_bin)
    result = []
    #
    if(pattern_length > array_length):
        return result
    if(pattern_length == 0):
        return result
    if(array_length == 0):
        return result
    #
    for i in range(array_length - pattern_length + 1):
        if array_bin[i:i + pattern_length] == pattern:
            result.append(i)
    #
    return result
#

def bin_find_pattern_in_2d_array(array_2d_bin, pattern):
    found = []
    if len(array_2d_bin)==0:
        return found
    for ar in array_2d_bin:
        pos = bin_find_pattern_in_1d_array(ar,pattern)
        found.append(pos)
    #
    return found
#

# 정수 비트의 개수 n_bit 가 주어지면, n_bit 크기의 모든 가능한 조합의 이진수 배열의 배열인 2차원 이진수 배열을 return
# n_bit 이 0 이하이면, 빈 배열을 return
def bin_generate_all_combination(n_bit):
    if n_bit <= 0:
        return []
    # 모든 가능한 조합 생성
    combinations = list(product([0, 1], repeat=n_bit))
    return [list(comb) for comb in combinations]


def bin_calculate_parity(bits, b_parity_odd):
    if len(bits) == 0:
        return -1
    """Calculate the parity bit of the given binary array."""
    parity_bit = sum(bits) % 2
    if b_parity_odd:
        return 1 - parity_bit  # Odd parity
    else:
        return parity_bit 
#

'''
bin_in : 1차원 또는 2차원 이진수 배열 (0 또는 1로 이루어진 배열)
b_parity_msb : True 이면, MSB 에 parity bit 추가, False 이면, LSB 에 parity bit 추가
'''
def bin_add_parity(bin_in, b_parity_msb, b_parity_odd):
    if len(bin_in) == 0:
        return []
    #
    if isinstance(bin_in[0], list):  # 2차원 배열인 경우
        return [
            [bin_calculate_parity(row, b_parity_odd)] + row if b_parity_msb else row + [bin_calculate_parity(row, b_parity_odd)]
            for row in bin_in
        ]
    else:  # 1차원 배열인 경우
        parity_bit = bin_calculate_parity(bin_in, b_parity_odd)
        return [parity_bit] + bin_in if b_parity_msb else bin_in + [parity_bit]

def bin_get_1d_from_2d(bin_2d):
    bin_1d = [bit for row in bin_2d for bit in row]
    return bin_1d
     
def bin_byte_to_binary_array(c,n_start=0, n_bit_size=8):
    # 바이트 값을 이진 문자열로 변환
    if n_start < 0 or n_start > 7:
        return []
    if n_bit_size <= 0 or n_bit_size > 8:
        return []
    #
    binary_string = f'{c:08b}'
    # 이진 문자열을 각 비트로 분리하여 배열로 변환
    binary_array = [int(bit) for bit in binary_string]
    sliced_ar = binary_array[n_start:n_start + n_bit_size]
    return sliced_ar

def bin_concate_1D_bin_to_2d_bin(bin_1d,bin_2d,b_concate_prefix):
    if len(bin_1d) == 0:
        return bin_2d
    if len(bin_2d) == 0:
        return []
    #
    result = []
    #
    for i in range(len(bin_2d)):
        if b_concate_prefix:
            result.append(bin_1d + bin_2d[i])
        else:
            result.append(bin_2d[i]+bin_1d)
    #
    return result

def bin_str_to_binary_array(s):
    return [int(char) for char in s if char in '01']

def bin_remove_matching_rows(bin_2d, pattern_1d):
    return [row for row in bin_2d if row != pattern_1d]


def bin_is_empty_2d_binary_array(ar_2d):
    if len(ar_2d) == 0:
        return True
    
    b_empty = True
    for ar_1d in ar_2d:
        if len(ar_1d) != 0:
            b_empty = False
            break
        #
    # end for
    return b_empty
#

def bin_get_2d_found_pattern(array_2d_bin, pattern):
    found_2d_bin = []
    found_index = bin_find_pattern_in_2d_array(array_2d_bin,pattern)
    if bin_is_empty_2d_binary_array(found_index):
        return found_2d_bin
    #
    for i in range(len(found_index)):
        if len(found_index[i]) > 0:
            ar_1d = array_2d_bin[i]
            #
            for index in found_index[i]:
                 ar_found = ar_1d[index:]
                 found_2d_bin.append(ar_found)
    #
    return found_2d_bin

def bin_print_2d( binary_2d_array, s_empty_cell="X" ):
    df = pd.DataFrame(binary_2d_array)
    df = df.map(lambda x: x if pd.notna(x) else s_empty_cell)
    df = df.map(lambda x: int(x) if (x is not s_empty_cell) and (x == 1.0 or x == 0.0) else x)
    print(df)


def bin_check_parity(array_bin, n_start_pos, n_bit_size, b_odd_parity):
    # 주어진 범위의 부분 배열 추출
    sub_array = array_bin[n_start_pos:n_start_pos + n_bit_size]
    
    # 부분 배열의 모든 비트의 합 계산
    bit_sum = sum(sub_array)
    
    # 패리티 계산
    if b_odd_parity:
        parity_bit = bit_sum % 2  # 홀수 패리티
        return parity_bit == 1
    else:
        parity_bit = bit_sum % 2  # 짝수 패리티
        return parity_bit == 0
    #
#