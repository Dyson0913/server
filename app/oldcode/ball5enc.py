 
# max bits > 0 == width of the value in bits (e.g., int_16 -> 16)
 
# Rotate left: 0b1001 --> 0b0011
rol = lambda val, r_bits, max_bits: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))
               
# Rotate right: 0b1001 --> 0b1100
ror = lambda val, r_bits, max_bits: \
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))
 

def encrypt_data(Key, text, length):
    KeyIndex = 0
    max_bits = 8
    for i in range(length):
        text[i] = rol(text[i], Key[KeyIndex], max_bits)
        text[i] ^= Key[KeyIndex]
        text[i] = ror(text[i], Key[KeyIndex], max_bits)
        KeyIndex += 1
        if KeyIndex == 16:
            KeyIndex = 0


def command_len(command):
    
    length = str(len(command))
    for i in range(4 - len(command)/10):
        length = "0" + length

    length += ";"

    return length


def encrypt_command(command, Key):

    buf = map(ord, command)

    #for i in range(len(buf)):
    #    print "0x%02x" % buf[i]

    #print "encrpyt====================="

    encrypt_data(Key, buf, len(buf))

    #for i in range(len(buf)):
    #    print "0x%02x" % buf[i]


    command_str = ""
    for i in range(len(buf)):
        command_str += "%02x" % buf[i]


    enc_command = command_len(command) + command_str.decode('hex')

    return enc_command

def decrypt_command(command, Key):

    #index = command.find(";")

    #length = int(command[:index])

    #length, enc_command = command.split(";")
    
    #length = int(length)

    #enc_command = command[index+1:]

    buf = map(ord, command)

    encrypt_data(Key, buf, len(buf))

    command_str = ""
    for i in range(len(buf)):
        command_str += "%02x" % buf[i]

    dec_command = command_str.decode('hex')


    return dec_command

if __name__ == '__main__':

    Key = [ 0x6A, 0x6B, 0x33, 0x16, 0x86, 0x62, 0x89, 0x71, 0x19, 0x39, 0x7C, 0x52, 0xF2, 0x1B, 0x88, 0xFC ]

    command = "100,1"

    enc_command = encrypt_command(command, Key)

    print enc_command
