import pandas as pd
import pyarrow as pa
import numpy as np
import itertools

# binary arrary operations module
# pyarrow version

# 
'''
@brief 
    PyArrow 1차원 배열의 모든 값을 반전, (0->1 또는 0->1).
@param
    array_bin - PyArrow 1차원 배열
@return
    반전된 PyArrow 1차원 배열
'''
def bin_invert_bits(array: pa.array) -> pa.array:
    # PyArrow 배열을 NumPy 배열로 변환
    numpy_array = array.to_numpy()
    
    # NumPy 배열에서 비트 반전 수행
    inverted_array = np.invert(numpy_array)
    
    # 반전된 배열을 다시 PyArrow 배열로 변환
    return pa.array(inverted_array)

'''
@brief 
    PyArrow 1차원 배열의 모든 값의 순서를 역전 시킨다.
@param
    array_bin - PyArrow 1차원 배열
@return
    순서가 역전된 PyArrow 1차원 배열
'''
def bin_invert_order(array: pa.Array) -> pa.Array:
    # pyarrow.Array에서 데이터를 NumPy 배열로 변환
    numpy_array = array.to_numpy()
    
    # 비트 순서를 반전 (NumPy 배열의 역순 슬라이싱)
    reversed_array = numpy_array[::-1]
    
    # 다시 pyarrow.Array로 변환
    return pa.array(reversed_array)


'''
@brief
    PyArrow 1차원 배열의 모든 값을 반전하고, (0->1 또는 0->1).
    모든 값의 순서를 역전 시킨다.
@param
    array_bin - PyArrow 1차원 배열
@return
    값이 반전되고, 순서가 역전된 PyArrow 1차원 배열
'''
def bin_invert_order_and_bits(array: pa.array) -> pa.array:
    # PyArrow 배열을 NumPy 배열로 변환
    numpy_array = array.to_numpy()
    
    # NumPy 배열에서 비트 반전 수행
    inverted_array = np.invert(numpy_array)
    
    # 비트 순서를 반전 (NumPy 배열의 역순 슬라이싱)
    reversed_array = inverted_array[::-1]
    
    # 반전된 배열을 다시 PyArrow 배열로 변환
    return pa.array(reversed_array)

'''
@brief 
    array_bin PyArrow 1차원 배열에서, pattern PyArrow 1차원 배열과 동일한 값들을 갖는 시작 인덱스의  PyArrow 1차원 배열를 반환.
@param
    array_bin - PyArrow 1차원 배열
    pattern - array_bin에서 찾는 PyArrow 1차원 배열
@return
    찾은 패턴의 시작 인덱스의 PyArrow 1차원 배열
'''
def bin_find_pattern_in_1d_array(array_bin: pa.array, pattern: pa.array) -> pa.Array:
    """
    Find all starting indices of the `pattern` in `array_bin`.

    Args:
        array_bin (pa.array): A pyarrow 1D array of binary values (0 or 1).
        pattern (pa.array): A pyarrow 1D array of binary values to search for.

    Returns:
        pa.array: A pyarrow 1D array of starting indices where the pattern is found in array_bin.
    """
    # Ensure input arrays are of type pyarrow.Array
    if not isinstance(array_bin, pa.Array) or not isinstance(pattern, pa.Array):
        raise TypeError("Both array_bin and pattern must be pyarrow arrays.")
    
    # Convert arrays to Python lists for processing
    array_bin_list = array_bin.to_pylist()
    pattern_list = pattern.to_pylist()
    
    # Length of the pattern
    pattern_len = len(pattern_list)
    if pattern_len == 0:
        raise ValueError("Pattern must not be empty.")
    
    # Find all start indices of the pattern in array_bin
    indices = [
        i for i in range(len(array_bin_list) - pattern_len + 1)
        if array_bin_list[i:i + pattern_len] == pattern_list
    ]
    
    # Convert the result to a pyarrow array
    return pa.array(indices)
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
def bin_find_pattern_in_2d_array(array_2d_bin: pa.ListArray, pattern: pa.array)->pa.ListArray:
    """
    Find all starting indices of the `pattern` in each row of a 2D pyarrow array.

    Args:
        array_2d_bin (pa.ListArray): A pyarrow 2D array of binary values (0 or 1).
        pattern (pa.Array): A pyarrow 1D array of binary values to search for.

    Returns:
        pa.ListArray: A pyarrow 2D array where each row contains the start indices of the pattern.
    """
    # Ensure the input array is a 2D pyarrow ListArray
    if not isinstance(array_2d_bin, pa.ListArray):
        raise TypeError("array_2d_bin must be a pyarrow ListArray.")
    
    # Ensure the pattern is a pyarrow Array
    if not isinstance(pattern, pa.Array):
        raise TypeError("pattern must be a pyarrow Array.")
    
    # Process each row in the 2D array
    result_indices = [
        bin_find_pattern_in_1d_array(row, pattern)
        for row in array_2d_bin
    ]
    
    # Convert results to a pyarrow ListArray
    return pa.list_array(result_indices)
#

'''
@brief 
    정수 비트의 개수 n_bit 가 주어지면, n_bit 크기의 모든 가능한 조합의 이진수 배열의 배열인 2차원 이진수 배열을 return
@param
    n_bit - 비트의 개수. n_bit 이 0 이하이면, 빈 배열을 return
@return
    2d - binary array. 
'''
def bin_generate_all_combination(n_bit)->pa.ListArray:
    """
    Generate all possible combinations of binary values for n_bit bits.

    Args:
        n_bit (int): The number of bits.

    Returns:
        pa.ListArray: A pyarrow 2D array containing all combinations of n_bit bits.
    """
    if n_bit <= 0:
        raise ValueError("n_bit must be a positive integer.")
    
    # Generate all combinations of n_bit binary values
    combinations = list(itertools.product([0, 1], repeat=n_bit))
    
    # Convert the combinations to a pyarrow ListArray
    return pa.array(combinations)
#

'''
@brief 
    1d binary array 에 대한 even or odd parity 계산.
@param
    bits - 패리티 계산 할 1d binary array.
    b_parity_odd - True 이면 odd parity 계산, False  이면 event parity 계산
@return
    -1 - bits 의 길이는 0, 1 또는 0 계산된 패리티 비트 값.
'''
def bin_calculate_parity(bits:pa.array, b_parity_odd):
    """
    Calculate the parity of a pyarrow 1D array.

    Args:
        bits (pa.Array): A pyarrow 1D array of binary values (0 or 1).
        b_parity_odd (bool): If True, calculate odd parity. If False, calculate even parity.

    Returns:
        int: 1 if the parity is odd (for odd parity) or needs to be 1 (for even parity),
             0 otherwise.
    """

    if not isinstance(bits, pa.Array):
        raise TypeError("bits must be a pyarrow Array.")

    # Ensure the array only contains 0 and 1
    if not all(bit in [0, 1] for bit in bits.to_pylist()):
        raise ValueError("bits must only contain binary values (0 or 1).")
    
    # Calculate the number of 1s
    num_ones = sum(bits.to_pylist())
    
    # Determine parity
    if b_parity_odd:
        # Odd parity: Check if the number of 1s is odd
        return 1 if num_ones % 2 == 0 else 0
    else:
        # Even parity: Check if the number of 1s is even
        return 0 if num_ones % 2 == 0 else 1
#

'''
@brief 
    요소값이 0,또는 1인 PyArrow 1차원 또는 PyArrow 2차원 배열에 parity 비트를 요소로 추가.
@param
    bin_in : parity bit를 추가 할, PyArrow 1차원 또는 2차원 배열 (0 또는 1로 이루어진 배열)
    b_parity_msb : True - parity bit 를 첫요소로 추가.  False - parity bit 를 마지막에 추가.
    b_parity_odd : Tur - odd parity 추가. False - even parity 추가.
@return
    parity 비트가 요소로 추가된 PyArrow 1차원 또는 2차원 배열
'''
def bin_add_parity(bin_in, b_parity_msb, b_parity_odd):
    """
    Add parity bits to a PyArrow 1D or 2D array.

    Args:
        bin_in (pa.Array or pa.ListArray): A PyArrow 1D or 2D array of binary values (0 or 1).
        b_parity_msb (bool): If True, add the parity bit as the first element. If False, add it as the last element.
        b_parity_odd (bool): If True, calculate odd parity. If False, calculate even parity.

    Returns:
        pa.Array or pa.ListArray: The input array with parity bits added.
    """
    if isinstance(bin_in, pa.ListArray):  # 2D Array
        result = []
        for row in bin_in:
            parity_bit = bin_calculate_parity(row, b_parity_odd)
            if b_parity_msb:
                result.append([parity_bit] + row.to_pylist())
            else:
                result.append(row.to_pylist() + [parity_bit])
        return pa.array(result)
    
    elif isinstance(bin_in, pa.Array):  # 1D Array
        parity_bit = bin_calculate_parity(bin_in, b_parity_odd)
        if b_parity_msb:
            return pa.array([parity_bit] + bin_in.to_pylist())
        else:
            return pa.array(bin_in.to_pylist() + [parity_bit])
    
    else:
        raise TypeError("bin_in must be a PyArrow 1D or 2D array.")
#

'''
@brief 
    pyarrow 2차원 이진수 배열 각 행의 끝에 다음행의 시작에 연결한 pyarrow 1차원 이진배열 생성. 
@param
    bin_2d - pyarrow 2차원 배열
@return
    binary array - 생성된 pyarrow 1차원 배열 
'''
def bin_get_1d_from_2d(bin_2d:pa.ListArray)->pa.array:
    """
    Create a PyArrow 1D binary array by concatenating all rows of a 2D binary array.

    Args:
        bin_2d (pa.ListArray): A PyArrow 2D array of binary values (0 or 1).

    Returns:
        pa.Array: A PyArrow 1D array containing concatenated binary values from the input 2D array.
    """
    if not isinstance(bin_2d, pa.ListArray):
        raise TypeError("bin_2d must be a PyArrow 2D array (ListArray).")

    # Convert the 2D array to a flat 1D list
    flattened_list = [item for row in bin_2d for item in row.to_pylist()]

    # Convert the list back to a PyArrow 1D array
    return pa.array(flattened_list)

'''
@brief 
    PyArrow 1차원 배열을 n_start index 부터,n_bit_size 개수 만튼 잘라 PyArrow 2차원 배열 생성.
@param
    bin_1d - PyArrow 1차원 배열
    n_bit_size - 생성될 PyArrow 2 차원 이진배열 각 행의 열 개수.
    n_start - bin_1d 에서 작업을 시작 할 요소의 인덱스 값.
@return
    생성된 PyArrow 2 차원 이진배열
'''
def bin_get_2d_from_1d(bin_1d:pa.array, n_bit_size, n_start=0)->pa.ListArray:
    """
    Create a PyArrow 2D binary array by slicing a PyArrow 1D array.

    Args:
        bin_1d (pa.Array): A PyArrow 1D array of binary values (0 or 1).
        n_bit_size (int): The number of columns for each row in the resulting 2D array.
        n_start (int, optional): The starting index in the 1D array. Defaults to 0.

    Returns:
        pa.ListArray: A PyArrow 2D array (ListArray) where each row has n_bit_size elements.
    """
    if not isinstance(bin_1d, pa.Array):
        raise TypeError("bin_1d must be a PyArrow 1D array.")

    if n_bit_size <= 0:
        raise ValueError("n_bit_size must be a positive integer.")

    if n_start < 0 or n_start >= len(bin_1d):
        raise ValueError("n_start must be within the bounds of the bin_1d array.")

    # Extract the relevant portion of the 1D array starting at n_start
    sliced_array = bin_1d.slice(n_start)

    # Convert the sliced array to a Python list
    sliced_list = sliced_array.to_pylist()

    # Group the elements into chunks of size n_bit_size
    grouped_list = [
        sliced_list[i:i + n_bit_size]
        for i in range(0, len(sliced_list), n_bit_size)
    ]

    # Convert the grouped list back to a PyArrow 2D ListArray
    return pa.array(grouped_list)
#

'''
@brief 
    1 바이트 값의 각 비트를 요소로하는 pyArrow 1차원 배열을 얻음.
@param
    c - 1바이트 값.
    n_start - c 에서 비트를 얻을 시작 위치(0~7)
    n_bit_size - c 에서 얻을 비트의 수(1~8)
@return
    pyArrow 1차원 이진배열
'''
def bin_get_binary_array_from_byte(c, n_start=0, n_bit_size=8)->pa.array:
    """
    Extract bits from a 1-byte value and return them as a PyArrow 1D binary array.

    Args:
        c (int): A 1-byte value (0 to 255).
        n_start (int, optional): The starting bit position (0 to 7). Defaults to 0.
        n_bit_size (int, optional): The number of bits to extract (1 to 8). Defaults to 8.

    Returns:
        pa.Array: A PyArrow 1D array containing the extracted bits (0 or 1).
    """
    # Validate inputs
    if not (0 <= c <= 255):
        raise ValueError("c must be a 1-byte value (0 to 255).")
    if not (0 <= n_start < 8):
        raise ValueError("n_start must be between 0 and 7.")
    if not (1 <= n_bit_size <= 8):
        raise ValueError("n_bit_size must be between 1 and 8.")
    if n_start + n_bit_size > 8:
        raise ValueError("n_start + n_bit_size must not exceed 8.")

    # Extract bits from the byte
    bits = [(c >> (7 - i)) & 1 for i in range(8)]  # Convert byte to a list of bits
    sliced_bits = bits[n_start:n_start + n_bit_size]  # Slice the desired bits

    # Convert the sliced bits to a PyArrow array
    return pa.array(sliced_bits)
#

'''
@brief 
    주어진 pyArrow 1차원 배열에서 지정된 크기만큼 잘라 bytearray로 변환합니다.
@param
    ar_1d_bin - pyArrow 1차원 배열
    n_start - ar_1d_bin에서 사용 할 요소의 시작 인데스(기본값: 0)
    n_bit_size - 1개의 바이트로 변환 할 ar_1d_bin의 요소의 수.(1~8)
    b_msb_first -  MSB 우선 여부 (True면 MSB 우선, False면 LSB 우선)
@return
    bytearray - 변환한 bytearray
'''
def bin_get_bytearray_from_binary_array(ar_1d_bin:pa.array, n_start=0, n_bit_size=8, b_msb_first=True)->bytearray:
    """
    Convert a PyArrow 1D binary array into a bytearray.

    Args:
        ar_1d_bin (pa.Array): PyArrow 1D binary array containing 0 or 1.
        n_start (int, optional): Starting index in the array. Defaults to 0.
        n_bit_size (int, optional): Number of bits to group into a single byte. Defaults to 8.
        b_msb_first (bool, optional): Whether to use MSB-first order. Defaults to True.

    Returns:
        bytearray: The resulting bytearray.
    """
    if not isinstance(ar_1d_bin, pa.Array):
        raise TypeError("ar_1d_bin must be a PyArrow 1D array.")

    if not all(bit in (0, 1) for bit in ar_1d_bin.to_pylist()):
        raise ValueError("ar_1d_bin must contain only binary values (0 or 1).")

    if n_bit_size < 1 or n_bit_size > 8:
        raise ValueError("n_bit_size must be between 1 and 8.")

    if n_start < 0 or n_start >= len(ar_1d_bin):
        raise ValueError("n_start must be within the bounds of ar_1d_bin.")

    # Slice the input array from the starting index
    sliced_array = ar_1d_bin.slice(n_start).to_pylist()

    # Group bits into chunks of size n_bit_size
    grouped_bits = [
        sliced_array[i:i + n_bit_size]
        for i in range(0, len(sliced_array), n_bit_size)
    ]

    # Convert each group of bits into a byte
    byte_array = bytearray()
    for bits in grouped_bits:
        # Pad with zeros if the group is smaller than n_bit_size
        if len(bits) < n_bit_size:
            bits += [0] * (n_bit_size - len(bits))

        # Convert bits to a single byte
        if b_msb_first:
            byte = sum(bit << (n_bit_size - 1 - i) for i, bit in enumerate(bits))
        else:
            byte = sum(bit << i for i, bit in enumerate(bits))

        byte_array.append(byte)

    return byte_array
#

'''
@brief 
    bin_1d 의 PyArrow 1차원 배열을 PyArrow 2차원 배열의 모든 행의 앞 또는 뒤에 추가.
@param
    bin_1d - 추가하는 PyArrow 1차원 array
    bin_2d - 추가되는 PyArrow 2차원 array
    b_concate_prefix - True 면 앞에 추가, False 이면 뒤에 추가.
@return
    추가된 PyArrow 2차원 배열.
'''
def bin_concate_1D_bin_to_2d_bin(bin_1d:pa.array, bin_2d:pa.ListArray, b_concate_prefix)->pa.ListArray:
    """
    Concatenate a PyArrow 1D binary array to the front or back of each row in a PyArrow 2D binary array.

    Args:
        bin_1d (pa.Array): PyArrow 1D array to concatenate.
        bin_2d (pa.Table): PyArrow 2D array to which the 1D array will be concatenated.
        b_concate_prefix (bool): If True, concatenate bin_1d to the front of each row; 
                                 if False, concatenate to the back.

    Returns:
        pa.Table: A new PyArrow 2D array with bin_1d concatenated.
    """
    # Validate inputs
    if not isinstance(bin_1d, pa.Array):
        raise TypeError("bin_1d must be a PyArrow 1D array.")
    if not isinstance(bin_2d, pa.Table):
        raise TypeError("bin_2d must be a PyArrow 2D array (pa.Table).")

    # Convert 1D array to a Python list
    bin_1d_list = bin_1d.to_pylist()

    # Prepare a new list for rows of the updated 2D array
    new_rows = []

    # Iterate over each row in the 2D array
    for row in bin_2d.to_pylist():
        if b_concate_prefix:
            # Concatenate 1D array to the front of each row
            new_row = bin_1d_list + row
        else:
            # Concatenate 1D array to the back of each row
            new_row = row + bin_1d_list
        new_rows.append(new_row)

    # Convert the updated list of rows back to a PyArrow 2D array
    result_table = pa.table(new_rows)

    return result_table
#

'''
@brief 
    ar_2d1 로 주어진 PyArrow 2차원 배열의 마지막 행 다음에 PyArrow 2차원 배열 ar_2d2 의 모든 행을 추가.
    열의 개수를 맞추기 위한 패딩은 없다.
@param
    ar_2d1 - 시작 PyArrow 2차원 배열
    ar_2d2 - ar_2d1 에 추가될 PyArrow 2차원 배열.
@return
    생성된 PyArrow 2차원 배열.
'''
def bin_concate_2d_bin_to_2d_bin(ar_2d1:pa.ListArray, ar_2d2:pa.ListArray)->pa.ListArray:
    """
    Concatenate all rows of a PyArrow 2D array (ar_2d2) to the end of another PyArrow 2D array (ar_2d1).

    Args:
        ar_2d1 (pa.Table): The starting PyArrow 2D array.
        ar_2d2 (pa.Table): The PyArrow 2D array to append to ar_2d1.

    Returns:
        pa.Table: A new PyArrow 2D array with ar_2d2 appended to ar_2d1.
    """
    # Validate inputs
    if not isinstance(ar_2d1, pa.Table):
        raise TypeError("ar_2d1 must be a PyArrow 2D array (pa.Table).")
    if not isinstance(ar_2d2, pa.Table):
        raise TypeError("ar_2d2 must be a PyArrow 2D array (pa.Table).")

    # Ensure the column count matches
    if ar_2d1.num_columns != ar_2d2.num_columns:
        raise ValueError("The number of columns in ar_2d1 and ar_2d2 must match.")

    # Concatenate the two tables
    concatenated_table = pa.concat_tables([ar_2d1, ar_2d2], promote=True)

    return concatenated_table
#

'''
@brief 
    문자 0, 1 로만 구성된 문자열로 부터 PyArrow 1차원 배열 생성.
@param
    s - 문자 0, 1 로만 구성된 문자열
@return
    생성된  PyArrow 1차원 배열.
'''
def bin_str_to_binary_array(s:str)->pa.array:
    """
    Convert a string composed of '0' and '1' characters into a PyArrow 1D binary array.

    Args:
        s (str): A string composed of '0' and '1' characters.

    Returns:
        pa.Array: A PyArrow 1D binary array.
    """
    # Validate input
    if not isinstance(s, str):
        raise TypeError("Input must be a string.")
    if not all(c in '01' for c in s):
        raise ValueError("Input string must contain only '0' and '1' characters.")

    # Convert the string to a list of integers (0 and 1)
    binary_list = [int(c) for c in s]

    # Create a PyArrow 1D array from the list
    binary_array = pa.array(binary_list, type=pa.int8())

    return binary_array
#

'''
@brief 
    주어진 PyArrow 2차원 배열의 행 중, PyArrow 1차원 배열로 주어진 패턴과 동일한 행을 삭제한 PyArrow 2차원 배열 얻기
@param
    bin_2d - PyArrow 2차원 배열
    pattern_1d - 패턴의 PyArrow 1차원 배열 
@return
    bin_2d 에서 pattern_1d 가 삭제된 PyArrow 2차원 배열.
'''
def bin_remove_matching_rows(bin_2d:pa.ListArray, pattern_1d:pa.array)->pa.ListArray:
    """
    Remove rows from a PyArrow 2D array that match a given 1D pattern.

    Args:
        bin_2d (pa.Table): A PyArrow 2D array (pa.Table).
        pattern_1d (pa.Array): A PyArrow 1D array representing the pattern to be removed.

    Returns:
        pa.Table: A new PyArrow 2D array with matching rows removed.
    """
    # Validate inputs
    if not isinstance(bin_2d, pa.Table):
        raise TypeError("bin_2d must be a PyArrow 2D array (pa.Table).")
    if not isinstance(pattern_1d, pa.Array):
        raise TypeError("pattern_1d must be a PyArrow 1D array.")
    if len(bin_2d.column_names) != len(pattern_1d):
        raise ValueError("The number of columns in bin_2d must match the length of pattern_1d.")

    # Convert pattern_1d to a Python list for comparison
    pattern_list = pattern_1d.to_pylist()

    # Filter rows that do not match the pattern
    filtered_rows = [
        row for row in bin_2d.to_pylist() if row != pattern_list
    ]

    # Convert the filtered rows back to a PyArrow table
    if filtered_rows:
        filtered_table = pa.table(filtered_rows, schema=bin_2d.schema)
    else:
        # If no rows remain, return an empty table with the same schema
        filtered_table = pa.table({col: [] for col in bin_2d.column_names})

    return filtered_table
#

'''
@brief 
    주어진 PyArrow 2차원 배열의 요소가 없거나, 모든 행의 길이가 0 이면 Ture.
@param
    ar_2d - PyArrow 2차원 배열
@return
    True or False 검사 결과
'''
def bin_is_empty_2d_binary_array(ar_2d:pa.ListArray):
    """
    Check if a PyArrow 2D array is empty or all rows have zero length.

    Args:
        ar_2d (pa.Table): A PyArrow 2D array.

    Returns:
        bool: True if the array is empty or all rows have zero length, False otherwise.
    """
    # Validate input
    if not isinstance(ar_2d, pa.Table):
        raise TypeError("Input must be a PyArrow 2D array (pa.Table).")

    # Check if the table is empty
    if ar_2d.num_rows == 0:
        return True

    # Check if all rows are empty
    for column in ar_2d.columns:
        if len(column) > 0:
            return False

    return True
#

'''
@brief 
    array_2d_bin 의 PyArrow 2차원 배열의 각 행에서, pattern 로 주아지는 PyArrow 1차원 배열과 일치하는 배열 시작 인데스를 모두 찾아 PyArrow 2차원 index 배열을 만듬. 
@param
    array_2d_bin - pattern 를 찾을 PyArrow 2차원 배열.
    pattern - 찾을 패턴의 PyArrow 1차원 배열
@return
    찾은 시작 인데스로 구성된 PyArrow 2차원 배열
'''
def bin_get_2d_found_pattern(array_2d_bin:pa.ListArray, pattern:pa.array)->pa.ListArray:
    """
    Find the start indices of a given pattern in each row of a PyArrow 2D binary array.

    Args:
        array_2d_bin (pa.Table): PyArrow 2D binary array.
        pattern (pa.Array): PyArrow 1D binary array pattern to search for.

    Returns:
        pa.Table: PyArrow 2D array of indices for each row where the pattern was found.
    """
    if not isinstance(array_2d_bin, pa.Table):
        raise TypeError("array_2d_bin must be a PyArrow 2D array (pa.Table).")
    if not isinstance(pattern, pa.Array):
        raise TypeError("pattern must be a PyArrow 1D array.")

    result_indices = []
    for column in array_2d_bin.columns:
        row_indices = bin_find_pattern_in_1d_array(column, pattern)
        result_indices.append(row_indices)

    # Convert the list of index arrays into a PyArrow table
    max_length = max(len(indices) for indices in result_indices) if result_indices else 0
    padded_indices = [
        list(indices) + [None] * (max_length - len(indices)) for indices in result_indices
    ]
    result_table = pa.table(padded_indices)

    return result_table
#

'''
@brief 
    주어진 PyArrow 2차원  배열을 0, 1 또는 값이 없는 부분은 s_empty_cell로 주어진 문자열로 pands 라이브러리를 이용해 문자 화면에 프린트.
@param
    binary_2d_array - 화면에 표시할 PyArrow 2차원 배열.
    s_empty_cell - 값이 없을 때 표시 할 문자열.(기본값 "X")
@return
    None
'''
def bin_print_2d( binary_2d_array:pa.ListArray, s_empty_cell="X" ):
    if not isinstance(binary_2d_array, pa.Table):
        raise TypeError("binary_2d_array must be a PyArrow 2D array (pa.Table).")

    # Convert the PyArrow Table to a Pandas DataFrame
    df = binary_2d_array.to_pandas()
    df = df.map(lambda x: x if pd.notna(x) else s_empty_cell)
    df = df.map(lambda x: int(x) if (x is not s_empty_cell) and (x == 1.0 or x == 0.0) else x)
    print(df)
#

'''
@brief 
    array_bin PyArrow 1차원 배열에서 n_start_pos 시작 인덱스 부터,  n_bit_size 개수 만큼의 인자로 PyArrow 1차원 배열을 생성하고,
    이 생성된 PyArrow 1차원 배열의 parity 비트를 검사 
@param
    array_bin - PyArrow 1차원 배열
    n_start_pos - array_bin 의 시작 인데스
    n_bit_size - 생성할 1차원 이진 배열의 크기
    b_odd_parity - True 면 odd parity 검사, False 면 even parity 검사
@return
    True - parity 검사 이상없음, False - parity 에러.
'''
def bin_check_parity(array_bin:pa.array, n_start_pos, n_bit_size, b_odd_parity):
    """
    Check the parity of a subset of a PyArrow 1D array.

    Args:
        array_bin (pa.Array): The PyArrow 1D binary array.
        n_start_pos (int): The starting index in the array.
        n_bit_size (int): The number of bits to consider from the starting index.
        b_odd_parity (bool): True for odd parity check, False for even parity check.

    Returns:
        bool: True if parity matches, False if there is a parity error.
    """
    if not isinstance(array_bin, pa.Array):
        raise TypeError("array_bin must be a PyArrow 1D array.")
    if n_start_pos < 0 or n_start_pos + n_bit_size > len(array_bin):
        raise ValueError("Invalid range specified for the subset of the array.")
    if n_bit_size <= 0:
        raise ValueError("n_bit_size must be greater than 0.")

    # Extract the subset of the array
    subset = array_bin.slice(n_start_pos, n_bit_size)

    # Count the number of 1s in the subset
    num_ones = sum(subset)

    # Check the parity
    if b_odd_parity:
        return num_ones % 2 == 1  # Odd parity: 1 if odd number of 1s
    else:
        return num_ones % 2 == 0  # Even parity: 1 if even number of 1s
    #
#

