'''
ISO1 or ISO2 or 3 track data generator!
'''

def calculate_odd_parity(value, n_bits):
    """Calculate odd parity for the given value based on n_bits."""
    count_ones = bin(value).count('1')
    if count_ones % 2 == 0:  # Even number of 1's, set parity bit
        value |= (1 << n_bits)
    return value

def display_binary(value, n_bits, reverse=False, invert=False):
    """Display binary representation of a value with options to reverse or invert."""
    binary = f"{value:0{n_bits}b}"
    if reverse:
        binary = binary[::-1]
    if invert:
        binary = ''.join('1' if bit == '0' else '0' for bit in binary)
    return binary

def get_bin_str(s_value, n_bits, reverse=False, invert=False, invert_byte_order=False):
    s_bin = ""
    for byte in s_value:
        s = display_binary(byte, n_bits + 1,reverse,invert)
        if invert_byte_order:
            s_bin = s + s_bin
        else:
            s_bin = s_bin + s
    #
    return s_bin

def get_asc_byte_from_user():
    # iso1 is
    # !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_
    # iso2 or 3 is
    #0123456789:;<=>?
    s_in = input("Enter a decoded data(ASCII): ")
    if(s_in == ""):
        s_in = "1234567890333458899912345678901111111"
        print("Default decoded data = ", s_in)

    # Convert string to ASCII byte array
    s_asc = bytearray(s_in, 'ascii')
    print("the size decoded data = ", len(s_asc))
    print("ASCII (hex):", '{', ', '.join(f"0x{byte:02X}" for byte in s_asc), '}')
    return s_asc
#

def get_data_bit_size_from_user():
    # Get n_bit value
    while True:
        try:
            user_input = input("Select data bit size (4 or 6): ")
            if user_input == "":
                n_bit = 4  # default data bit size
                break
            n_bit = int(user_input)
            if n_bit in (4, 6):
                break
            else:
                print("Invalid choice. Enter 4 or 6.")
        except ValueError:
            print("Please enter a valid number.")
    #
    print("the bit size = ", n_bit)
    return n_bit
#

def get_stx_etx(n_bit_size):
    if n_bit_size == 4:
        c_stx = 0x0B
        c_etx = 0x0F
    else:
        c_stx = 0x05
        c_etx = 0x1F
    #
    return c_stx, c_etx
#

def get_iso_data(s_asc, n_bit):
    # Convert ASCII to ISO and process
    s_iso = bytearray()
    offset = 0x30 if n_bit == 4 else 0x20

    for byte in s_asc:
        s_iso.append(byte - offset)

    print("\nISO (hex, before parity):", '{', ', '.join(f"0x{byte:02X}" for byte in s_iso), '}')
    return s_iso
#

def add_stx_etx_lrc(s_iso, c_stx, c_etx):
    s_pre = bytearray()
    s_pre.append(c_stx)
    s_iso = s_pre + s_iso
    s_iso.append(c_etx)

    # Calculate c_lrc
    c_lrc = 0x00
    for byte in s_iso:
        c_lrc ^= byte  # XOR each byte into c_lrc
    #
    s_iso.append(c_lrc)
    print("\nISO (hex, added stx,etx,lrc):", '{', ', '.join(f"0x{byte:02X}" for byte in s_iso), '}')
    return s_iso
#

def hex_string_to_bytearray(hex_str):
    # Convert hex string to bytearray
    byte_array = bytearray.fromhex(hex_str)
    return byte_array

def bytearray_to_bin_string(byte_array):
    # Convert bytearray to binary string
    bin_str = ''.join(f"{byte:08b}" for byte in byte_array)
    return bin_str

def hex_string_to_bin_string(hex_str):
    # Convert hex string to binary string
    byte_array = hex_string_to_bytearray(hex_str)
    bin_str = bytearray_to_bin_string(byte_array)
    # print("Binary string:", bin_str)
    return bin_str

def find_substring_positions(s_in, s_sub):
    positions = []
    start = 0
    while True:
        start = s_in.find(s_sub, start)
        if start == -1:
            break
        positions.append(start)
        start += 1  # Move past the last found substring
    return positions


def get_bin_string_encoder_data_from_user():
    s_hex = input("Enter a encoder string(HEX): ")
    if(s_hex == ""):
        # s_hex = "0000AC2026A9F6A00CE79CA42294730E62926A0FCA3084104208DF010000C0"
        s_hex = "FFFFCAFB9B6A90FACF18C6DABBD6318FB9B6A90FACF3DEF7BDEF047FFFFF"
        print("Default encoder data = ", s_hex)
    #
    print("the size encoded data = ", len(s_hex), "bytes")
    s_bin = hex_string_to_bin_string(s_hex)
    print("the number of bits encoded data = ", len(s_bin), "bits")
    
    print(s_bin)
    return s_bin
#

def main():
    # get encoder card data from user
    s_bin_encoder = get_bin_string_encoder_data_from_user()

    # get decoded card data from user
    s_asc = get_asc_byte_from_user()

    # Get n_bit value
    n_bit = get_data_bit_size_from_user()

    # Convert ASCII to ISO and process
    s_iso = get_iso_data(s_asc, n_bit)

    # Add STX , ETX and LRC
    c_stx, c_etx = get_stx_etx(n_bit)
    s_iso = add_stx_etx_lrc(s_iso, c_stx, c_etx)

    # Apply parity
    s_iso = bytearray(calculate_odd_parity(byte, n_bit) for byte in s_iso)
    print("\nISO (hex, after parity):", '{', ', '.join(f"0x{byte:02X}" for byte in s_iso), '}')

    ####################################################################
    # Display binary representations
    print("the length of data = ", len(s_iso))
    ##################################
    b_bit_reverse = False
    b_bit_invert = False
    b_byte_reverse = False
    print("\nMSB -> LSB:")
    #print('{', ', '.join(f"{display_binary(byte, n_bit + 1,b_bit_reverse,b_bit_invert)}" for byte in s_iso), '}')
    s_bin_msb_lsb = get_bin_str(s_iso,n_bit,b_bit_reverse,b_bit_invert,b_byte_reverse)
    print("the number of bits encoded data = ", len(s_bin_msb_lsb), "bits")
    print(s_bin_msb_lsb)

    pos = find_substring_positions(s_bin_encoder, s_bin_msb_lsb)
    print("the positions = ", pos)

    ##################################
    b_bit_reverse = False
    b_bit_invert = True
    b_byte_reverse = False
    print("\nInverted(MSB -> LSB):")
    #print('{', ', '.join(f"{display_binary(byte, n_bit + 1,b_bit_reverse,b_bit_invert)}" for byte in s_iso), '}')
    s_bin_msb_lsb_inv = get_bin_str(s_iso,n_bit,b_bit_reverse,b_bit_invert,b_byte_reverse)
    print("the number of bits encoded data = ", len(s_bin_msb_lsb_inv), "bits")
    print(s_bin_msb_lsb_inv)

    pos = find_substring_positions(s_bin_encoder, s_bin_msb_lsb_inv)
    print("the positions = ", pos)
    
    ##################################
    b_bit_reverse = True
    b_bit_invert = False
    b_byte_reverse = False
    print("\nLSB -> MSB:")
    #print('{', ', '.join(f"{display_binary(byte, n_bit + 1,b_bit_reverse,b_bit_invert)}" for byte in s_iso), '}')
    s_bin_lsb_msb = get_bin_str(s_iso,n_bit,b_bit_reverse,b_bit_invert,b_byte_reverse)
    print("the number of bits encoded data = ", len(s_bin_lsb_msb), "bits")
    print(s_bin_lsb_msb)

    pos = find_substring_positions(s_bin_encoder, s_bin_lsb_msb)
    print("the positions = ", pos)

    ##################################
    b_bit_reverse = True
    b_bit_invert = True
    b_byte_reverse = False
    print("\nInverted (LSB -> MSB):")
    #print('{', ', '.join(f"{display_binary(byte, n_bit + 1, b_bit_reverse,b_bit_invert)}" for byte in s_iso), '}')
    s_bin_lsb_msb_inv = get_bin_str(s_iso,n_bit,b_bit_reverse,b_bit_invert,b_byte_reverse)
    print("the number of bits encoded data = ", len(s_bin_lsb_msb_inv), "bits")
    print(s_bin_lsb_msb_inv)

    pos = find_substring_positions(s_bin_encoder, s_bin_lsb_msb_inv)
    print("the positions = ", pos)

    ########### byte order reverse ##################################
    ##################################
    b_bit_reverse = False
    b_bit_invert = False
    b_byte_reverse = True
    print("\nByte-INV-MSB -> LSB:")
    #print('{', ', '.join(f"{display_binary(byte, n_bit + 1,b_bit_reverse,b_bit_invert)}" for byte in s_iso), '}')
    s_bin_msb_lsb = get_bin_str(s_iso,n_bit,b_bit_reverse,b_bit_invert,b_byte_reverse)
    print("the number of bits encoded data = ", len(s_bin_msb_lsb), "bits")
    print(s_bin_msb_lsb)

    pos = find_substring_positions(s_bin_encoder, s_bin_msb_lsb)
    print("the positions = ", pos)

    ##################################
    b_bit_reverse = False
    b_bit_invert = True
    b_byte_reverse = True
    print("\nByte-INV-Inverted(MSB -> LSB):")
    #print('{', ', '.join(f"{display_binary(byte, n_bit + 1,b_bit_reverse,b_bit_invert)}" for byte in s_iso), '}')
    s_bin_msb_lsb_inv = get_bin_str(s_iso,n_bit,b_bit_reverse,b_bit_invert,b_byte_reverse)
    print("the number of bits encoded data = ", len(s_bin_msb_lsb_inv), "bits")
    print(s_bin_msb_lsb_inv)

    pos = find_substring_positions(s_bin_encoder, s_bin_msb_lsb_inv)
    print("the positions = ", pos)
    
    ##################################
    b_bit_reverse = True
    b_bit_invert = False
    b_byte_reverse = True
    print("\nByte-INV-LSB -> MSB:")
    #print('{', ', '.join(f"{display_binary(byte, n_bit + 1,b_bit_reverse,b_bit_invert)}" for byte in s_iso), '}')
    s_bin_lsb_msb = get_bin_str(s_iso,n_bit,b_bit_reverse,b_bit_invert,b_byte_reverse)
    print("the number of bits encoded data = ", len(s_bin_lsb_msb), "bits")
    print(s_bin_lsb_msb)

    pos = find_substring_positions(s_bin_encoder, s_bin_lsb_msb)
    print("the positions = ", pos)

    ##################################
    b_bit_reverse = True
    b_bit_invert = True
    b_byte_reverse = True
    print("\nByte-INV-Inverted (LSB -> MSB):")
    #print('{', ', '.join(f"{display_binary(byte, n_bit + 1, b_bit_reverse,b_bit_invert)}" for byte in s_iso), '}')
    s_bin_lsb_msb_inv = get_bin_str(s_iso,n_bit,b_bit_reverse,b_bit_invert,b_byte_reverse)
    print("the number of bits encoded data = ", len(s_bin_lsb_msb_inv), "bits")
    print(s_bin_lsb_msb_inv)

    pos = find_substring_positions(s_bin_encoder, s_bin_lsb_msb_inv)
    print("the positions = ", pos)

if __name__ == "__main__":
    main()
