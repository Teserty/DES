import random

def gcd(a, b):
    """
    Performs the Euclidean algorithm and returns the gcd of a and b
    """
    if (b == 0):
        return a
    else:
        return gcd(b, a % b)

def xgcd(a, b):
    """
    Performs the extended Euclidean algorithm
    Returns the gcd, coefficient of a, and coefficient of b
    """
    x, old_x = 0, 1
    y, old_y = 1, 0

    while (b != 0):
        quotient = a // b
        a, b = b, a - quotient * b
        old_x, x = x, old_x - quotient * x
        old_y, y = y, old_y - quotient * y

    return a, old_x, old_y

def chooseE(totient):
    """
    Chooses a random number, 1 < e < totient, and checks whether or not it is 
    coprime with the totient, that is, gcd(e, totient) = 1
    """
    while (True):
        e = random.randrange(2, totient)

        if (gcd(e, totient) == 1):
            return e

def chooseKeys():
    """
    Selects two random prime numbers from a list of prime numbers which has 
    values that go up to 100k. It creates a text file and stores the two 
    numbers there where they can be used later. Using the prime numbers, 
    it also computes and stores the public and private keys in two separate 
    files.
    """

    # choose two random numbers within the range of lines where 
    # the prime numbers are not too small and not too big
    rand1 = random.randint(100, 300)
    rand2 = random.randint(100, 300)

    # store the txt file of prime numbers in a python list
    fo = open('primes-to-100k.txt', 'r')
    lines = fo.read().splitlines()
    fo.close()

    # store our prime numbers in these variables
    prime1 = int(lines[rand1])
    prime2 = int(lines[rand2])

    # compute n, totient, e
    n = prime1 * prime2
    totient = (prime1 - 1) * (prime2 - 1)
    e = chooseE(totient)

    # compute d, 1 < d < totient such that ed = 1 (mod totient)
    # e and d are inverses (mod totient)
    gcd, x, y = xgcd(e, totient)

    # make sure d is positive
    if (x < 0):
        d = x + totient
    else:
        d = x

    # write the public keys n and e to a file
    f_public = open('public_keys.txt', 'w')
    f_public.write(str(n) + '\n')
    f_public.write(str(e) + '\n')
    f_public.close()

    f_private = open('private_keys.txt', 'w')
    f_private.write(str(n) + '\n')
    f_private.write(str(d) + '\n')
    f_private.close()

def encrypt(message, file_name = 'public_keys.txt', block_size = 2):
    """
    Encrypts a message (string) by raising each character's ASCII value to the 
    power of e and taking the modulus of n. Returns a string of numbers.
    file_name refers to file where the public key is located. If a file is not 
    provided, it assumes that we are encrypting the message using our own 
    public keys. Otherwise, it can use someone else's public key, which is 
    stored in a different file.
    block_size refers to how many characters make up one group of numbers in 
    each index of encrypted_blocks.
    """

    try:
        fo = open(file_name, 'r')

    # check for the possibility that the user tries to encrypt something
    # using a public key that is not found
    except FileNotFoundError:
        print('That file is not found.')
    else:
        n = int(fo.readline())
        e = int(fo.readline())
        fo.close()

        encrypted_blocks = []
        ciphertext = -1

        if (len(message) > 0):
            # initialize ciphertext to the ASCII of the first character of message
            ciphertext = ord(message[0])

        for i in range(1, len(message)):
            # add ciphertext to the list if the max block size is reached
            # reset ciphertext so we can continue adding ASCII codes
            if (i % block_size == 0):
                encrypted_blocks.append(ciphertext)
                ciphertext = 0

            # multiply by 1000 to shift the digits over to the left by 3 places
            # because ASCII codes are a max of 3 digits in decimal
            ciphertext = ciphertext * 1000 + ord(message[i])

        # add the last block to the list
        encrypted_blocks.append(ciphertext)

        # encrypt all of the numbers by taking it to the power of e
        # and modding it by n
        for i in range(len(encrypted_blocks)):
            encrypted_blocks[i] = str((encrypted_blocks[i]**e) % n)

        # create a string from the numbers
        encrypted_message = " ".join(encrypted_blocks)

        return encrypted_message

def decrypt(blocks, block_size = 2):
    """
    Decrypts a string of numbers by raising each number to the power of d and 
    taking the modulus of n. Returns the message as a string.
    block_size refers to how many characters make up one group of numbers in
    each index of blocks.
    """

    fo = open('private_keys.txt', 'r')
    n = int(fo.readline())
    d = int(fo.readline())
    fo.close()

    # turns the string into a list of ints
    list_blocks = blocks.split(' ')
    int_blocks = []

    for s in list_blocks:
        int_blocks.append(int(s))

    message = ""

    # converts each int in the list to block_size number of characters
    # by default, each int represents two characters
    for i in range(len(int_blocks)):
        # decrypt all of the numbers by taking it to the power of d
        # and modding it by n
        int_blocks[i] = (int_blocks[i]**d) % n
        
        tmp = ""
        # take apart each block into its ASCII codes for each character
        # and store it in the message string
        for c in range(block_size):
            tmp = chr(int_blocks[i] % 1000) + tmp
            int_blocks[i] //= 1000
        message += tmp

    return message


# In[13]:


choose_again = input('Do you want to generate new public and private keys? (y or n) ')
if (choose_again == 'y'):
    chooseKeys()

instruction = input('Would you like to encrypt or decrypt? (Enter e or d): ')
if (instruction == 'e'):
    message = input('What would you like to encrypt?\n')
    option = input('Do you want to encrypt using your own public key? (y or n) ')

    if (option == 'y'):
        print('Encrypting...')
        print(encrypt(message))
    else:
        file_option = input('Enter the file name that stores the public key: ')
        print('Encrypting...')
        print(encrypt(message, file_option))

elif (instruction == 'd'):
    message = input('What would you like to decrypt?\n')
    print('Decryption...')
    print(decrypt(message))
else:
    print('That is not a proper instruction.')


# In[3]:


import sys
import binascii

PC1 = [57,  49,  41,  33,  25,  17,   9,
        1,  58,  50,  42,  34,  26,  18,
       10,   2,  59,  51,  43,  35,  27,
       19,  11,   3,  60,  52,  44,  36,
       63,  55,  47,  39,  31,  23,  15,
        7,  62,  54,  46,  38,  30,  22,
       14,   6,  61,  53,  45,  37,  29,
       21,  13,   5,  28,  20,  12,   4]

PC2 = [14,  17,  11,  24,   1,   5,
       3,   28,  15,   6,  21,  10,
       23,  19,  12,   4,  26,   8,
       16,   7,  27,  20,  13,   2,
       41,  52,  31,  37,  47,  55,
       30,  40,  51,  45,  33,  48,
       44,  49,  39,  56,  34,  53,
       46,  42,  50,  36,  29,  32]

LSHIFT_MAP = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

IP = [58,  50,  42,  34,  26,  18,  10,   2,
      60,  52,  44,  36,  28,  20,  12,   4,
      62,  54,  46,  38,  30,  22,  14,   6,
      64,  56,  48,  40,  32,  24,  16,   8,
      57,  49,  41,  33,  25,  17,   9,   1,
      59,  51,  43,  35,  27,  19,  11,   3,
      61,  53,  45,  37,  29,  21,  13,   5,
      63,  55,  47,  39,  31,  23,  15,   7]

E = [32,   1,   2,   3,   4,   5,
      4,   5,   6,   7,   8,   9,
      8,   9,  10,  11,  12,  13,
     12,  13,  14,  15,  16,  17,
     16,  17,  18,  19,  20,  21,
     20,  21,  22,  23,  24,  25,
     24,  25,  26,  27,  28,  29,
     28,  29,  30,  31,  32,   1]

SBOXES = {0:
            [[14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7],
             [ 0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8],
             [ 4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0],
             [15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13]],
          1:
            [[15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10],
             [ 3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5],
             [ 0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15],
             [13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9]],
          2:
            [[10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8],
             [13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1],
             [13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7],
             [ 1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12]],
          3:
            [[ 7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15],
             [13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9],
             [10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4],
             [ 3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14]],
          4:
            [[ 2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9],
             [14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6],
             [ 4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14],
             [11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3]],
          5:
            [[12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11],
             [10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8],
             [ 9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6],
             [ 4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13]],
          6:
            [[ 4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1],
             [13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6],
             [ 1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2],
             [ 6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12]],
          7:
            [[13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7],
             [ 1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2],
             [ 7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8],
             [ 2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11]]}

P = [16,   7,  20,  21,
     29,  12,  28,  17,
      1,  15,  23,  26,
      5,  18,  31,  10,
      2,   8,  24,  14,
     32,  27,   3,   9,
     19,  13,  30,   6,
     22,  11,   4,  25]

IP_INVERSE = [40,   8,  48,  16,  56,  24,  64,  32,
              39,   7,  47,  15,  55,  23,  63,  31,
              38,   6,  46,  14,  54,  22,  62,  30,
              37,   5,  45,  13,  53,  21,  61,  29,
              36,   4,  44,  12,  52,  20,  60,  28,
              35,   3,  43,  11,  51,  19,  59,  27,
              34,   2,  42,  10,  50,  18,  58,  26,
              33,   1,  41,   9,  49,  17,  57,  25]


def hex_to_64binary(hexstr):
    """convert a hex string to a 64 bit wide binary number"""
    try:
        int64 = long(hexstr, 16)
    except ValueError:
        raise ValueError('ERROR: can not convert %s to base 16.' % hexstr)

    bin64 = str(bin(int64))[2:].rjust(64, '0')

    return bin64


def binary_to_hex(binstr):
    """convert a binary string to a hex"""
    hexstr = []

    for i in range(0, len(binstr), 4):
        total = 0
        binstr_rev = [x for x in reversed(binstr[i:i+4])]
        for j in range(4):
            total += (2**j) * int(binstr_rev[j])
        hexstr.append('%X' % total)

    return ''.join(hexstr)


def string_chunker(label, value, break_at=None):
    """print a label/value pair and insert a space in the value at break_at
    intervals
    """
    if break_at == None:
        s = value
    else:
        s = []
        for i in range(0, len(value), break_at):
            for ii in range(break_at):
                s.append(value[i+ii])
            s.append(' ')

        s = ''.join(map(str, s[:-1]))

    return '%s: %s' % (label.ljust(10), s)


def lshift(c, d, iteration):
    """left shift bits N times according to the LSHIFT_MAP (where N is the
    value at LSHIFT_MAP[iteration]; append knocked off bit(s) to end of string
    """
    for i in range(LSHIFT_MAP[iteration]):
        c = '%s%s' % (c[1:], c[0])
        d = '%s%s' % (d[1:], d[0])

    return (c, d)


def permutate(permutation, in_bits, out_bits_wide):
    """Map the bits contained within in_bits to a new bit string out_bits
    according to some permutation.
    1) iterate through the permutation
    1) for each value, in_bits_i, in the permutation
    2) map the value at in_bits[in_bits_i] to out_bits[iteration]
    """
    out_bits = [-1] * out_bits_wide
    for i in range(len(permutation)):
        in_bits_i = permutation[i] - 1
        out_bits[i] = in_bits[in_bits_i]

    return ''.join(map(str, out_bits))


def xor(bits1, bits2):
    """xor bits1 bit string with bits2 bit string; also used for 2bit addition.
    Truth Table for XOR (think of T=1 and F=0...)
    T T = F
    T F = T
    F T = T
    F F = F
    """
    bits = []

    for i in range(len(bits1)):
        b1 = int(bits1[i])
        b2 = int(bits2[i])
        xor_bit = int(bool(b1) ^ bool(b2))
        bits.append(xor_bit)

    return ''.join(map(str, bits))


def message_to_hex(msg):
    """convert an ASCII string to (uppercase) Hex"""
    hexstr = []

    for c in msg:
        hexstr.append('%X' % ord(c))

    return ''.join(hexstr)


def get_hexwords(msg):
    """break the ASCII message into a 64bit (16 hex bytes) words"""
    hexwords = []

    for i in range(0, len(msg), 8):
        msg_block = msg[i:i+8]
        m = message_to_hex(msg_block)
        hexwords.append(m)

    last = hexwords[-1]
    hexwords[-1] += ''.join(['0'] * (16-len(last)))

    # TODO - remove
    #hexwords = ['0123456789ABCDEF']

    return hexwords


def encrypt(key, msg):
    """break the message string down into hexwords and encrypt each"""
    encrypted_msg = []

    for hexword in get_hexwords(msg):
        #print string_chunker('encrypting hexword', hexword, 2)
        encrypted_msg.append(encrypt_hexword(key, hexword))

    return ''.join(encrypted_msg)


def encrypt_hexword(key, hexword):
    """run a given hexword through the DES algorithm and return the encrypted
    hex string
    """
    # message
    m = hex_to_64binary(hexword)
    #print string_chunker('M', m, 4)

    # key
    k = hex_to_64binary(key)
    #print string_chunker('K', k, 8)

    # initial permutation of message
    ip = permutate(IP, m, 64)
    #print string_chunker('IP', ip, 8)

    middle = len(ip) / 2
    l = ip[:middle]
    r = ip[middle:]
    #print string_chunker('l', l, 4)
    #print string_chunker('r', r, 4)

    # apply PC1 permutation to the key and split in half to form c and d
    cd = permutate(PC1, k, 56)
    middle = len(cd) / 2
    c = cd[:middle]
    d = cd[middle:]
    #print string_chunker('cd:', cd, 7)
    #print string_chunker('c0:', c, 7)
    #print string_chunker('d0:', d, 7)

    #print '-'*80

    # loop 16 'rounds'
    for round_i in range(16):

        # left shift the bits of c and d
        (c, d) = lshift(c, d, round_i)
        #print string_chunker('c%d' % (round_i+1), c, 7)
        #print string_chunker('d%d' % (round_i+1), d, 7)

        # apply PC2 permutation
        k = permutate(PC2, c+d, 48)
        #print string_chunker('k%d' % (round_i+1), k, 6)

        # apply E permutation
        e = permutate(E, r, 48)
        #print string_chunker('E(R%d)' % (round_i), e, 6)

        # xor k with e (2 bit addition)
        x = xor(k, e)
        #print string_chunker('xor(K%d,E(R%d)' % (round_i+1, round_i), x, 6)

        # apply SBOX permutations to blocks of 6 values of the result of the
        # previous XOR.
        s = []
        for n in range(len(x) / 6):
            start = 6 * n
            end = (6 * n) + 6
            b = x[start:end]
            i = int(b[0])*2**1 + int(b[-1])*2**0
            j = (int(b[1])*2**3 + int(b[2])*2**2 +
                 int(b[3])*2**1 + int(b[4])*2**0)
            s.append(str(bin(SBOXES[n][i][j]))[2:].rjust(4, '0'))
        s = ''.join(s)
        #print string_chunker('S%d' % (round_i+1), s, 4)

        # apply P permutation.
        f = permutate(P, s, 32)
        #print string_chunker('f%d' % (round_i+1), f, 4)

        # save value of l to calculate r (because the r bits have to get
        # shifted into l before we calculate the new r)
        l_prev = l

        # shift r into l (both 32 bits)
        l = r
        #print string_chunker('L%s' % (round_i+1), l, 4)

        # the new 32 bits of r are the saved value of l XORed/added to the value
        # of f
        r = xor(l_prev, f)
        #print string_chunker('R%d' % (round_i+1), r, 4)

        #print '-'*80

    # reverse left/right
    rl = '%s%s' % (r, l)
    #print string_chunker('rl', rl, 8)

    # apply the IP_INVERSE permutation
    encrypted_msg =  permutate(IP_INVERSE, rl, 64)
    #print string_chunker('enc msg', encrypted_msg, 8)

    # convert the final bitstring back into a hex message
    bin2hex = binary_to_hex(encrypted_msg)
    #print string_chunker('hex', bin2hex)

    return bin2hex


def run():
    file = open("public_keys.txt","r+")
    key = file.read().replace('\n','')
    file1 = open("text.txt", "r+")
    
    msg = file1.read()
    #print ('key:', key)
    #print ('msg:', msg)
    
    file3 = open("encr.txt", "w+")
    
    enc = encrypt(key, msg)
    file3.write(enc)
    
    print (string_chunker('encrypted:', enc, 16))

run()


# In[ ]:
