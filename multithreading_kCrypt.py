"""threading support for kCrypt

"""

import threading
from queue import Queue
import time
import random

import kCrypt
import textConvert

lock = threading.Lock()
#keys = kCrypt.generate_keys(1024, 2048)
keys = ((2249879, 61), (2249879, 368341))
#keys = ((3233, 17), (3233, 2753))
sequence = "word1 word2 word3"
print("sequence: ", sequence)

numeral_sequence = textConvert.convert_to_numerals(sequence)
print("numeral_sequence: ", numeral_sequence)

enumerated_sequence = dict(enumerate(kCrypt.split_by_n(numeral_sequence, 2)))
print(enumerated_sequence)

encrypted_sequence = {} 
print(encrypted_sequence)

decrypted_sequence = {}

def encryptJob(worker):
    encrypted_sequence[worker] = kCrypt.encrypt(int(enumerated_sequence[worker]), keys[0])

    with lock:
        print("%s, encrypt_worker: %s, result: %s, time: %s" % (threading.current_thread().name, worker, encrypted_sequence[worker], time.time()-start))

def decryptJob(worker):
    decrypted_sequence[worker] = kCrypt.decrypt(int(encrypted_sequence[worker]), keys[1])

    with lock:
        print("%s, decrypt_worker: %s, result: %s, time: %s" % (threading.current_thread().name, worker, decrypted_sequence[worker], time.time()-start))

def threader():
    while True:
        worker = q.get()
        encryptJob(worker)
        q.task_done()

def decrypt_threader():
    while True:
        worker = dq.get()
        decryptJob(worker)
        dq.task_done()

q = Queue()

for x in range(10):
    t = threading.Thread(target = threader)
    t.daemon = True
    t.start()

start = time.time()

for worker in enumerated_sequence:
    q.put(worker)

q.join()

print(encrypted_sequence)

dq = Queue()

for x in range(10):
    dt = threading.Thread(target = decrypt_threader)
    dt.daemon = True
    dt.start()

for worker in encrypted_sequence:
    dq.put(worker)

dq.join()

print(decrypted_sequence)

print("entire job took: ", time.time()-start)