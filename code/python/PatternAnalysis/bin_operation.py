import pandas as pd

# binary arrary operations module

from itertools import product

# 
'''
@brief 
    invert all bits of the given binary array.
@param
    array_bin - 1d binary array
@return
    binary array
'''
def bin_invert_bits(array_bin):
    return [1 - bit for bit in array_bin]

'''
@brief 
    invert the bits order of the given binary array.
@param
    array_bin - 1d binary array
@return
    binary array
'''
def bin_invert_order(array_bin):
    return array_bin[::-1]


'''
@brief 
    invert the order of the given binary array.
    invert all bits of the given binary array.
@param
    array_bin - 1d binary array
@return
    binary array
'''
def bin_invert_order_and_bits(array_bin):
    return [1 - bit for bit in array_bin][::-1]

'''
@brief 
    find pattern in the given binary array.
@param
    array_bin - 1d binary array
    pattern - 1d binary array. the founding pattern.
@return
    binary array. - the indexs array of the found patterns
'''
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

'''
@brief 
    find pattern in the given 2d binary array.
@param
    array_2d_bin - 2d binary array
    pattern - 1d binary array. the founding pattern.
@return
    2d binary array. - the 2d indexs array of the found patterns
'''
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

'''
@brief 
    정수 비트의 개수 n_bit 가 주어지면, n_bit 크기의 모든 가능한 조합의 이진수 배열의 배열인 2차원 이진수 배열을 return
@param
    n_bit - 비트의 개수. n_bit 이 0 이하이면, 빈 배열을 return
@return
    2d - binary array. 
'''
def bin_generate_all_combination(n_bit):
    if n_bit <= 0:
        return []
    # 모든 가능한 조합 생성
    combinations = list(product([0, 1], repeat=n_bit))
    return [list(comb) for comb in combinations]

'''
@brief 
    1d binary array 에 대한 even or odd parity 계산.
@param
    bits - 패리티 계산 할 1d binary array.
    b_parity_odd - True 이면 odd parity 계산, False  이면 event parity 계산
@return
    -1 - bits 의 길이는 0, 1 또는 0 계산된 패리티 비트 값.
'''
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
@brief 
    1차원 또는 2차원 이진수 배열에 parity 비트를 추가.
@param
    bin_in : parity bit를 추가 할, 1차원 또는 2차원 이진수 배열 (0 또는 1로 이루어진 배열)
    b_parity_msb : True - parity bit 를 MSB 에 추가.  False - parity bit 를 LSB 에 추가.
@return
    parity 비트가 추가된 1차원 또는 2차원 이진수 배열
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

'''
@brief 
    2차원 이진수 배열 각 행의 끝을 다음해의 시작에 연결한 1차원 이진배열 생성. 
@param
    bin_2d - 2차원 이진수 배열
@return
    binary array - 생성된 1차원 이진배열 
'''
def bin_get_1d_from_2d(bin_2d):
    bin_1d = [bit for row in bin_2d for bit in row]
    return bin_1d

'''
@brief 
    1차원 이진배열을 n_start index 부터,n_bit_size 개수 만튼 잘라 2차원 이진배열 생성.
@param
    bin_1d - 1d binary array
    n_bit_size - 생성될 2 차원 이진배열 각 행의 열 개수.
    n_start - bin_1d 에서 작업을 시작 할 요소의 인덱스 값.
@return
    생성된 2 차원 이진배열
'''
def bin_get_2d_from_1d(bin_1d, n_bit_size,n_start = 0):
    bin_2d = []
    #
    if len(bin_1d)==0:
        return bin_2d
    if n_bit_size <=0:
        return bin_2d
    #
    for i in range(n_start, len(bin_1d), n_bit_size):
        bin_2d.append(bin_1d[i:i + n_bit_size])
    return bin_2d
#

'''
@brief 
    1 바이트 값에 해당하는 이진 배열을 얻음.
@param
    c - 1바이트 값.
    n_start - c 에서 비트를 얻을 시작 위치(0~7)
    n_bit_size - c 에서 얻을 비트의 수(1~8)
@return
    1차원 이진배열
'''
def bin_get_binary_array_from_byte(c,n_start=0, n_bit_size=8):
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

'''
@brief 
    주어진 이진 배열에서 지정된 크기만큼 잘라 바이트 배열로 변환합니다.
@param
    ar_1d_bin - 1차원 이진배열
    n_start - ar_1d_bin에서 사용 할 요소의 시작 인데스(기본값: 0)
    n_bit_size - 1개의 바이트로 변환 할 ar_1d_bin의 요소의 수.(1~8)
    b_msb_first -  MSB 우선 여부 (True면 MSB 우선, False면 리틀엔디언)
@return
    bytearray - 변환한 bytearray
'''
def bin_get_bytearray_from_binary_array(ar_1d_bin, n_start=0, n_bit_size=8, b_msb_first=True):
    byte_array = bytearray()
    n = len(ar_1d_bin)

    # n_start부터 n_bit_size씩 처리
    for i in range(n_start, n, n_bit_size):
        # 잘라낼 비트 구간
        bits = ar_1d_bin[i:i + n_bit_size]

        # 비트가 부족하면 0으로 채움
        if len(bits) < n_bit_size:
            bits.extend([0] * (n_bit_size - len(bits)))

        # MSB 우선인지 리틀엔디언인지 확인
        if not b_msb_first:
            bits = bits[::-1]  # 리틀엔디언일 경우 비트 순서 반전

        # 비트를 문자열로 변환 후 정수로 변환
        byte_value = int("".join(map(str, bits)), 2)
        byte_array.append(byte_value)

    return byte_array
#

'''
@brief 
    bin_1d 의 1차원 배열을 이차원 배열의 모든 1차원 배열 요수의 앞 또는 뒤애 추가.
@param
    bin_1d - 추가하는 1d binary array
    bin_2d - 추가되는 2d binary array
    b_concate_prefix - True 면 앞에 추가, False 이면 뒤에 추가.
@return
    추가된 이차원 배열.
'''
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

'''
@brief 
    ar_2d1 로 주어진 2차원 배열의 마지막 행 다음에 ar_2d2 의 모든 행을 추가.
    열의 개수를 마추기 위한 패딩은 없다.
@param
    ar_2d1 - 시작 이차원 배열
    ar_2d2 - ar_2d1 에 추가될 이차원 배열.
@return
    연결된 2차원 배열.
'''
def bin_concate_2d_bin_to_2d_bin(ar_2d1, ar_2d2):
    combined_array = []

    # 첫 번째 배열의 각 행을 결합된 배열에 추가
    for row in ar_2d1:
        combined_array.append(row)
    
    # 두 번째 배열의 각 행을 결합된 배열에 추가
    for row in ar_2d2:
        combined_array.append(row)

    return combined_array
#

'''
@brief 
    문자 0, 1 로만 구성된 문자열을 1차원 이진배열.
@param
    s - 문자 0, 1 로만 구성된 문자열
@return
    생성된  1차원 이진배열.
'''
def bin_str_to_binary_array(s):
    return [int(char) for char in s if char in '01']

'''
@brief 
    주어진 이차원 배열의 행 중, 1차원 배열로 주어진 패턴과 동일한 행을 삭제한 이차원 배열 얻기
@param
    bin_2d - 2d binary array
    pattern_1d - 패턴의 1차원 배열 
@return
    bin_2d 에서 pattern_1d 가 삭제된 이차원 배열.
'''
def bin_remove_matching_rows(bin_2d, pattern_1d):
    return [row for row in bin_2d if row != pattern_1d]


'''
@brief 
    주어진 이차원 배열가 없거나, 이차원 배열의 모든 요소인 1차원 배열의 길이가 0 이면 Ture.
@param
    ar_2d - 2d binary array
@return
    True or False 검사 결과
'''
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

'''
@brief 
    array_2d_bin 의 이차원 배열의 각 행에서, pattern 로 주아지는 1차원 배열과 일치하는 배열 시작 인데스를 모두 찾아 이 차원 index 배열을 만듬. 
@param
    array_2d_bin - pattern 를 찾을 2차원 배열.
    pattern - 찾을 패턴의 2차원 배열
@return
    찾은 시작 인데스로 구성된 이차원 배열
'''
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

'''
@brief 
    주어진 이차원 이진 배열을 0, 1 , 값이 얻는 부분은 s_empty_cell로 주어진 pands 라이브러리를 이용해 문자 화면에 프린트.
@param
    binary_2d_array - 화면에 표시할 이차원 이진배열.
    s_empty_cell - 값이 없을 때 표시 할 문자열.(기본값 "X")
@return
    None
'''
def bin_print_2d( binary_2d_array, s_empty_cell="X" ):
    df = pd.DataFrame(binary_2d_array)
    df = df.map(lambda x: x if pd.notna(x) else s_empty_cell)
    df = df.map(lambda x: int(x) if (x is not s_empty_cell) and (x == 1.0 or x == 0.0) else x)
    print(df)


'''
@brief 
    array_bin 1차원 이진 배열에서 n_start_pos 시작 인덱스 부터,  n_bit_size 개수 만큼의 인자로 1차원 이진 배열을 생성하고,
    이 생성된 1차원 이진 배열의 parity 비트를 검사 
@param
    array_bin - 1d binary array
    n_start_pos - array_bin 의 시작 인데스
    n_bit_size - 생성할 1차원 이진 배열의 크기
    b_odd_parity - True 면 odd parity 검사, False 면 even parity 검사
@return
    True - parity 검사 이상없음, False - parity 에러.
'''
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

