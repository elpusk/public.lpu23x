import numpy as np
import pandas as pd
from itertools import product

#
def bin_invert_bits(array_bin):
    return np.logical_not(array_bin).astype(int)

def bin_invert_order(array_bin):
    return np.flip(array_bin)

def bin_invert_order_and_bits(array_bin):
    return np.flip(np.logical_not(array_bin).astype(int))

def bin_find_pattern_in_1d_array(array_bin, pattern):
    pattern_length = len(pattern)
    array_length = len(array_bin)
    if pattern_length > array_length or pattern_length == 0 or array_length == 0:
        return np.array([])
    return np.array([i for i in range(array_length - pattern_length + 1) if np.array_equal(array_bin[i:i + pattern_length], pattern)])

def bin_find_pattern_in_2d_array(array_2d_bin, pattern):
    return np.array([bin_find_pattern_in_1d_array(row, pattern) for row in array_2d_bin])

def bin_generate_all_combination(n_bit):
    if n_bit <= 0:
        return np.array([])
    return np.array(list(product([0, 1], repeat=n_bit)))

def bin_calculate_parity(bits, b_parity_odd):
    if len(bits) == 0:
        return -1
    parity_bit = np.sum(bits) % 2
    return 1 - parity_bit if b_parity_odd else parity_bit

def bin_add_parity(bin_in, b_parity_msb, b_parity_odd):
    if len(bin_in) == 0:
        return np.array([])
    if isinstance(bin_in[0], (list, np.ndarray)):
        return np.array([
            np.insert(row, 0, bin_calculate_parity(row, b_parity_odd)) if b_parity_msb else np.append(row, bin_calculate_parity(row, b_parity_odd))
            for row in bin_in
        ])
    else:
        parity_bit = bin_calculate_parity(bin_in, b_parity_odd)
        return np.insert(bin_in, 0, parity_bit) if b_parity_msb else np.append(bin_in, parity_bit)

def bin_get_1d_from_2d(bin_2d):
    return np.concatenate(bin_2d)

def bin_get_2d_from_1d(bin_1d, n_bit_size, n_start=0):
    if len(bin_1d) == 0 or n_bit_size <= 0:
        return np.array([])
    return np.array([bin_1d[i:i + n_bit_size] for i in range(n_start, len(bin_1d), n_bit_size)])

def bin_get_binary_array_from_byte(c, n_start=0, n_bit_size=8):
    if n_start < 0 or n_start > 7 or n_bit_size <= 0 or n_bit_size > 8:
        return np.array([])
    binary_string = np.binary_repr(c, width=8)
    return np.array(list(map(int, binary_string[n_start:n_start + n_bit_size])))

def bin_get_bytearray_from_binary_array(ar_1d_bin, n_start=0, n_bit_size=8, b_msb_first=True):
    byte_array = bytearray()
    n = len(ar_1d_bin)
    for i in range(n_start, n, n_bit_size):
        bits = ar_1d_bin[i:i + n_bit_size]
        if len(bits) < n_bit_size:
            bits = np.pad(bits, (0, n_bit_size - len(bits)), constant_values=0)
        if not b_msb_first:
            bits = np.flip(bits)
        byte_value = int("".join(map(str, bits)), 2)
        byte_array.append(byte_value)
    return byte_array

def bin_concate_1D_bin_to_2d_bin(bin_1d, bin_2d, b_concate_prefix):
    if len(bin_1d) == 0:
        return bin_2d
    if len(bin_2d) == 0:
        return np.array([])
    return np.array([
        np.concatenate([bin_1d, row]) if b_concate_prefix else np.concatenate([row, bin_1d])
        for row in bin_2d
    ])

def bin_concate_2d_bin_to_2d_bin(ar_2d1, ar_2d2):
    return np.vstack((ar_2d1, ar_2d2))

def bin_str_to_binary_array(s):
    return np.array([int(char) for char in s if char in '01'])

def bin_remove_matching_rows(bin_2d, pattern_1d):
    return np.array([row for row in bin_2d if not np.array_equal(row, pattern_1d)])

def bin_is_empty_2d_binary_array(ar_2d):
    return len(ar_2d) == 0 or all(len(row) == 0 for row in ar_2d)

def bin_get_2d_found_pattern(array_2d_bin, pattern):
    found_2d_bin = np.array([])
    found_index = bin_find_pattern_in_2d_array(array_2d_bin, pattern)
    for i, indices in enumerate(found_index):
        for index in indices:
            np.append(found_2d_bin, array_2d_bin[i][index:])
    return np.array(found_2d_bin)

def bin_print_2d(binary_2d_array, s_empty_cell="X"):
    df = pd.DataFrame(binary_2d_array)
    df = df.fillna(s_empty_cell)
    print(df.replace({1.0: 1, 0.0: 0}).to_string(index=False, header=False))

def bin_check_parity(array_bin, n_start_pos, n_bit_size, b_odd_parity):
    sub_array = array_bin[n_start_pos:n_start_pos + n_bit_size]
    bit_sum = np.sum(sub_array)
    return (bit_sum % 2 == 1) if b_odd_parity else (bit_sum % 2 == 0)
