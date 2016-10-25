"""
K-Crypt encryption module, by Kyle Koivukangas
just messing around in Python, thought RSA encryption would be a fun little challenge.

TODO: 
	- add config file for settings like decrypt chunk size and prime range
	- make faster (incredibly slow bare minimum first build)
	- have script store keys into a file
"""



import random
import textConvert

def full_test():
	#series of prints and function runs to test kCrypt as a whole	
	message = "word1 word2 word3"
	print "message: %s" % message

	numeral_message = textConvert.convert_to_numerals(message)
	print "numeral_message: %s" % numeral_message

	encrypted_sequence = split_encrypt(numeral_message, encrypt_chunk_size)
	print "encrypted_sequence: %s" % encrypted_sequence

	decrypted_sequence = split_decrypt(encrypted_sequence, encrypt_chunk_size)
	print "decrypted_sequence: %s" % decrypted_sequence

	decrypted_message = textConvert.convert_to_alpha(decrypted_sequence)
	print "decrypted_message: %s" % decrypted_message


#this function checks to see if the argument is a prime number or not
def isPrime(n):
    for x in range(2, n):
        if n % x == 0:
            return False
    return True

#This function generates a list of primes up to the number provided in the argument (inclusive).
def primeList(start, stop): 			
	if stop == 2: return [2]
	elif start < 3: start = 3
	return [x for x in range(start, stop) if isPrime(x)]

#this funtion calls on the primelist function to generate a list of primes within the 
#parameters, then returns two random indices of that list that are close togethero
def randomPrime(start, stop):		
	list_of_primes = primeList(start, stop)
	random_indice = random.randint(0, (len(list_of_primes)-4)) #subtract extra to balance next lines addition so you don't go out of range
	return list_of_primes[random_indice], list_of_primes[random_indice+3]

#this function returns the greatest common denominator of the two perameters given
def greatest_common_denominator(a, b):
  while a * b:
    if a > b:
      a %= b
    else:
      b %= a
  return max(a, b)

#this function tests whether the two numbers given are coprime or not
def isCoprime(a, b):
  return greatest_common_denominator(a, b) == 1

#this function returns a list of coprimes of the given number
def coprimeList(n):
	return [x for x in range(3, n, 2) if isCoprime(x, n)]

def find_public_exponent(n):
	list_of_coprimes = coprimeList(n)
	return list_of_coprimes[random.randint(0, 50)] #first 50 indices of coprimes

def find_private_exponent(n, e):
	for d in range(3, n, 2):
		if d * e % n == 1:
			return d

#generates RSA keys with primes originating from the range of the given parameters 
def generate_keys(prime_range_start, prime_range_stop):
	p, q = randomPrime(prime_range_start, prime_range_stop)
	# q = randomPrime(prime_range_start, prime_range_stop)
	n = (p - 1) * (q - 1)
	e = find_public_exponent(n)
	d = find_private_exponent(n, e)
	#print "\np: %s    q: %s    = n: %s\ne = %s    d = %s" % (p, q, n, e, d) #debug print
	public_key = (p*q, e)
	private_key = (p*q, d)
	return (public_key, private_key)

# c = m ** e % n
def encrypt(message, public_key):
	n, e = public_key[0], public_key[1]
	#print "encryption commencing... public_key = n: %s e: %s" % (n, e)
	return message**e % n

# m = c ** e % n
def decrypt(crypto_message, private_key):
	n, d = private_key[0], private_key[1]
	#print "decryption commencing... private_key = n: %s d: %s" % (n, d)
	return crypto_message**d % n

def split_by_n(sequence, n):
	#generator splits a sequence by n
    while sequence:
        yield sequence[:n]
        sequence = sequence[n:]

def split_encrypt(message, n):
	#encrypts a sequence in sections (n) and returns the joined result
	message = list(split_by_n(message, n))
	encrypted_message = []
	for i in range(len(message)):
		encrypted_message.append(encrypt(int(message[i]), keys[0]))
	return encrypted_message

def split_decrypt(encrypted_message, n):
	#derypts a sequence in secions (n) and returns the joined result
	decrypted_message = []
	for i in range(len(encrypted_message)):
		decrypted_message.append(decrypt(int(encrypted_message[i]), keys[1]))
	return ''.join(textConvert.convert_long_list_to_string_list(decrypted_message))

#keys = generate_keys(1024, 2048)
#print keys
#keys = ((2249879, 61), (2249879, 368341))  #debug keys
keys = ((3233, 17), (3233, 2753))

encrypt_chunk_size = 1

if __name__ == '__main__':
	full_test()





