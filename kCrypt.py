"""
K-Crypt encryption module, by Kyle Koivukangas
just messing around in Python, thought RSA encryption would be a fun little challenge.
I'm basically just following this https://simple.wikipedia.org/wiki/RSA_(algorithm)#Encrypting_messages

TODO: 
    - add config file for settings like encrypt chunk size and prime range
    - make faster (incredibly slow bare minimum first build)
    - have script store keys into a file
"""

import random

import textConvert

def full_test():
    """series of prints and function calls to test kCrypt as a whole    """

    sequence = "word1 word2 word3"
    print "sequence: %s" % sequence

    numeral_sequence = textConvert.convert_to_numerals(sequence)
    print "numeral_sequence: %s" % numeral_sequence

    encrypted_sequence = split_encrypt(numeral_sequence, encrypt_chunk_size)
    print "encrypted_sequence: %s" % encrypted_sequence

    decrypted_sequence = split_decrypt(encrypted_sequence, encrypt_chunk_size)
    print "decrypted_numeral_sequence: %s" % decrypted_sequence

    decrypted_sequence = textConvert.convert_to_alpha(decrypted_sequence)
    print "decrypted_sequence: %s" % decrypted_sequence


def generate_keys(prime_range_start, prime_range_stop):
    """generates RSA keys as tuples the original primes used to generate the keys are generated from a range between the given parameters"""
    p, q = randomPrime(prime_range_start, prime_range_stop)
    n = (p - 1) * (q - 1)
    e = find_public_exponent(n)
    d = find_private_exponent(n, e)
    public_key = (p*q, e)
    private_key = (p*q, d)
    return (public_key, private_key)

def randomPrime(start, stop):
    """generates a tuple of two random prime numbers within the range of the given parameters (start, stop)"""
    list_of_primes = primeList(start, stop)
    #random_indice = random.choice(list_of_primes) #subtract extra to balance next lines addition so you don't go out of range
    return random.choice(list_of_primes), random.choice(list_of_primes)

def primeList(start, stop): 
    """Generates a list of prime numbers between the two given parameters (start, stop)"""    
    if stop == 2: return [2]
    elif start < 3: start = 3
    return [x for x in range(start, stop) if isPrime(x)]

def isPrime(n):
    """tests whether a number is prime or not"""
    for x in range(2, n):
        if n % x == 0:
            return False
    return True


def find_public_exponent(n):
    """calculates the public key exponent ('e') for the RSA encryption algorithm"""
    list_of_coprimes = coprimeList(n)
    return list_of_coprimes[random.randint(0, 50)] #first 50 indices of coprimes

def coprimeList(n):
    """returns a list of coprimes of a number"""
    return [x for x in range(3, n, 2) if isCoprime(x, n)]

def isCoprime(a, b):
    """tests whether two numbers are coprime or not"""
    return greatest_common_denominator(a, b) == 1

def greatest_common_denominator(a, b):
    """returns the greatest common denominator of the two given numbers"""
    while a * b:
        if a > b:
            a %= b
        else:
            b %= a
    return max(a, b)


def find_private_exponent(n, e):
    """calculates the private key exponent ('d') for the RSA encryption algorithm"""
    for d in range(3, n, 2):
        if d * e % n == 1:
            return d


def encrypt(sequence, public_key):
    """encrypts a sequence with RSA encryption(c = m ** e % n) where m = message sequence (m, public_key)"""
    n, e = public_key[0], public_key[1]
    return sequence**e % n


def decrypt(crypto_sequence, private_key):
    """decrypts a sequence with RSA encryption (m = c ** e % n) where c = encrypted sequence (c, private_key)"""
    n, d = private_key[0], private_key[1]
    return crypto_sequence**d % n


def split_by_n(sequence, n):
    """generator splits a sequence by n (sequence, n)"""
    while sequence:
        yield sequence[:n]
        sequence = sequence[n:]


def split_encrypt(sequence, n):
    """encrypts a sequence in n sized chunks and returns the list result (sequence, n)"""
    sequence = list(split_by_n(sequence, n))
    encrypted_sequence = []
    for i in range(len(sequence)):
        encrypted_sequence.append(encrypt(int(sequence[i]), keys[0]))
    return encrypted_sequence


def split_decrypt(encrypted_sequence, n):
    """derypts a sequence in n sized chunks and returns the joined result (encrypted_sequence, n)"""
    decrypted_sequence = []
    for i in range(len(encrypted_sequence)):
        decrypted_sequence.append(decrypt(int(encrypted_sequence[i]), keys[1]))
    return ''.join(textConvert.convert_long_list_to_string_list(decrypted_sequence))


encrypt_chunk_size = 1

if __name__ == '__main__':

    keys = generate_keys(1024, 2048)
    #print keys
    #keys = ((2249879, 61), (2249879, 368341))  #debug keys
    #keys = ((3233, 17), (3233, 2753))

    full_test()





