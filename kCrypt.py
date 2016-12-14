"""K-Crypt encryption module, by Kyle Koivukangas
just messing around in Python, thought RSA encryption would be a fun little challenge.
I'm basically just following this https://simple.wikipedia.org/wiki/RSA_(algorithm)#Encrypting_messages

TODO: 
    - add config file for settings like encrypt chunk size and prime range
    - make faster (incredibly slow bare minimum first build)
    - have script store keys into a file

testing VS Code Git integration..
"""

import random

import textConvert

_encrypt_chunk_size = 1


def full_test():
    """series of prints and function calls to test kCrypt as a whole    """

    sequence = "word1 word2 word3"
    print "sequence: %s" % sequence

    numeral_sequence = textConvert.convert_to_numerals(sequence)
    print "numeral_sequence: %s" % numeral_sequence

    encrypted_sequence = split_encrypt(numeral_sequence, _encrypt_chunk_size)
    print "encrypted_sequence: %s" % encrypted_sequence

    decrypted_sequence = split_decrypt(encrypted_sequence)
    print "decrypted_numeral_sequence: %s" % decrypted_sequence

    decrypted_sequence = textConvert.convert_to_alpha(decrypted_sequence)
    print "decrypted_sequence: %s" % decrypted_sequence


def generate_keys(prime_range_start, prime_range_stop):
    """generates RSA keys as tuples the original primes used to generate the keys are generated from a range between the given parameters"""
    prime1, prime2 = random_prime(prime_range_start, prime_range_stop)
    modulus = prime1 * prime2
    totient = (prime1 - 1) * (prime2 - 1)
    public_exponent = find_public_exponent(totient)
    private_exponent = find_private_exponent(totient, public_exponent)
    public_key = (modulus, public_exponent)
    private_key = (modulus, private_exponent)
    return (public_key, private_key)


def random_prime(start, stop):
    """generates a tuple of two random prime numbers within the range of the given parameters (start, stop)"""
    list_of_primes = prime_list(start, stop)
    # random_indice = random.choice(list_of_primes) #subtract extra to balance
    # next lines addition so you don't go out of range

    return random.choice(list_of_primes), random.choice(list_of_primes)


def prime_list(start, stop):
    """Generates a list of prime numbers between the two given parameters (start, stop)"""
    if stop == 2:
        return [2]
    elif start < 3:
        start = 3
    return [x for x in range(start, stop) if is_prime(x)]


def is_prime(number):
    """tests whether a number is prime or not"""
    for i in range(2, number):
        if number % i == 0:
            return False
    return True


def find_public_exponent(totient):
    """calculates the public key exponent ('e') for the RSA encryption algorithm"""
    list_of_coprimes = coprime_list(totient)
    # chooses from the first 50 indices of coprimes to keep the numbers
    # relatively close
    return list_of_coprimes[random.randint(0, 50)]


def coprime_list(totient):
    """returns a list of coprimes of a number"""
    return [x for x in range(3, totient, 2) if is_coprime(x, totient)]


def is_coprime(a, b):
    """tests whether two numbers are coprime or not (coprime if GCD == 1)"""
    return greatest_common_denominator(a, b) == 1


def greatest_common_denominator(a, b):
    """returns the greatest common denominator of the two given numbers"""
    while a * b:
        if a > b:
            a %= b
        else:
            b %= a
    return max(a, b)


def find_private_exponent(totient, public_exponent):
    """calculates the private key exponent ('d') for the RSA encryption algorithm"""
    for i in range(3, totient, 2):
        if i * public_exponent % totient == 1:
            return i


def encrypt(sequence, public_key):
    """encrypts a sequence with RSA encryption(c = m ** e % n) where m = message sequence (m, public_key)"""
    modulus, public_exponent = public_key[0], public_key[1]
    return sequence**public_exponent % modulus


def decrypt(crypto_sequence, private_key):
    """decrypts a sequence with RSA encryption (m = c ** e % n) where c = encrypted sequence (c, private_key)"""
    modulus, private_exponent = private_key[0], private_key[1]
    return crypto_sequence**private_exponent % modulus


def split_by_n(sequence, n):
    """generator splits a sequence by 'n' characters (sequence, n)"""
    while sequence:
        yield sequence[:n]
        sequence = sequence[n:]


def split_encrypt(sequence, split_size):
    """encrypts a sequence of chunks and returns the result as a list (sequence, n)"""
    sequence = list(split_by_n(sequence, split_size))
    encrypted_sequence = []
    for i, item in enumerate(sequence):
        encrypted_sequence.append(encrypt(int(sequence[i]), keys[0]))
    return encrypted_sequence


def split_decrypt(encrypted_sequence):
    """decrypts a chunked sequence and returns the joined result (encrypted_sequence)"""
    decrypted_sequence = []
    for i, item in enumerate(encrypted_sequence):
        decrypted_sequence.append(decrypt(int(encrypted_sequence[i]), keys[1]))
    return ''.join(textConvert.convert_long_list_to_string_list(decrypted_sequence))


if __name__ == '__main__':

    keys = generate_keys(1024, 2048)
    # print keys
    # keys = ((2249879, 61), (2249879, 368341))  #debug keys
    #keys = ((3233, 17), (3233, 2753))

    full_test()
else:
    # else statement to temporarily add debug keys for when calling kCrypt to test threading
    #keys = ((2249879, 61), (2249879, 368341))
    keys = ((3233, 17), (3233, 2753))