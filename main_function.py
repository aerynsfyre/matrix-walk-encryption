#!/usr/bin/env python3
import secrets
import binascii
import time
import random
import string
from sys import getsizeof
import numpy as np

# encrypt
def encrypt(plaintext, key_matrix, key_matrix_two, modulus):
	if isinstance(plaintext, str):
		plain = bytes((plaintext), 'utf-8')
		int_plain = [0]*len(plain)
		index = 0
		for i in plain:
			int_plain[index] = (int(i))
			index = index+1
		print(int_plain)
	else:
		plain = plaintext
	x = 0
	index = 0
	loc_x = 0
	loc_y = 0
	ciphertext = [0]*len(plain)
	for i in plain:
		xored = i^(key_matrix[loc_x%modulus][loc_y%modulus])
		xored_bin = format(xored, '08b')
		current = xored_bin[(len(xored_bin)-2):]
		movement = int(xored_bin[:len(xored_bin)-2],base=2)%modulus
		if current=='00':
			loc_y = (loc_y+movement)%modulus
		elif current=='11':
			loc_y = (loc_y-movement)%modulus
		elif current=='01':
			loc_x = (loc_x+movement)%modulus
		elif current=='10':
			loc_x = (loc_x-movement)%modulus
		xored = xored^(key_matrix_two[loc_x%modulus][loc_y%modulus])
		ciphertext[index] = xored
		index = index+1
	ciphertext.extend([loc_x,loc_y])
	return ciphertext
	
# decrypt
def decrypt(ciphertext, key_matrix, key_matrix_two, modulus):
	x = 0
	index = len(ciphertext)-3
	loc_x = ciphertext[(len(ciphertext)-2)]
	loc_y = ciphertext[(len(ciphertext)-1)]
	plain = [0]*(len(ciphertext)-2)
	while index >= 0:
		xored = ciphertext[index]^key_matrix_two[loc_x%modulus][loc_y%modulus]
		plain_bin = format(xored, '08b')
		current = plain_bin[(len(plain_bin)-2):]
		movement = int(plain_bin[:len(plain_bin)-2],base=2)%modulus
		if current=='00':
			loc_y = (loc_y-movement)%modulus
		if current=='11':
			loc_y = (loc_y+movement)%modulus
		if current=='01':
			loc_x = (loc_x-movement)%modulus
		if current=='10':
			loc_x = (loc_x+movement)%modulus
		plain[index] = xored^key_matrix[loc_x%modulus][loc_y%modulus]
		index = index-1
	return plain
	
	
# generate key matrix
def get_key_matrix(size):
	key = [0]*size
	key_rows = [0]*size
	i = 0
	while i < size:
		j = 0
		while j < size:
			key_rows[j] = secrets.randbits(8)
			j = j+1
		key[i] = key_rows.copy()
		i = i+1
	for s in key_rows:
		key
	return key
	
def change_bit(plain):
	plain_altered = [0]*len(plain)
	plain_bytes =  bytes((plain), 'utf-8')
	x = 0
	for i in plain_bytes:
		plain_altered[x] = format(i, '08b')
		x = x+1
	random_byte = random.randint(0,(len(plain)-1))
	random_bit = random.randint(0,(len(plain_altered[random_byte])-1))
	to_change = plain_altered[random_byte]
	altered = ''
	x = 0
	for i in to_change:
		if x == random_bit:
			if i == '0':
				altered = altered+'1'
			if i == '1':
				altered = altered+'0'
		else:
			altered=altered+i
		x=x+1
	x = 0
	#alt = (int(altered,base=2))
	plain_altered[random_byte] = altered
	#alt_plain = alt.to_bytes().decode()
	for i in plain_altered:
		plain_altered[x] = int(i,base=2)
		x=x+1
	#plain_altered[random_byte] = alt_plain
	plain_string = ''
	for i in plain_altered:
		plain_string = plain_string+chr(i)
	#print(plain)
	#print((plain_string))
	return plain_string
    
def get_difference(one, two, size):
	j = 0
	diff = 0
	x = 0
	while j<len(one):
		if one[j] != two[j]:
			diff = diff+1
		j = j+1
	difference = (diff/len(one))*100
	#print("Number of different bytes: "+str(diff))
	#print("Length of string: "+str(len(one)))
	return difference

# main
def main():
	size = 32
	plaintext_size = 16
	start = time.process_time()
	key_matrix = get_key_matrix(size)
	key_matrix_two = get_key_matrix(size)
	stop = time.process_time()
	key_generation_time = stop-start
	#size = getsizeof(key_matrix) + getsizeof(key_matrix_two)
	#print("Memory required for key matrices: "+str(size))
	#print("Key Matrix Generated. Time taken: "+str(key_generation_time))
	#print(key_matrix)
	#for i in key_matrix:
	#	print(i)
	plaintext = ''.join(random.choices(string.ascii_lowercase, k=plaintext_size))#input("Enter plaintext to encrypt: ")
	start = time.process_time()
	print(plaintext)
	print(bytes(plaintext, "utf-8"))
	cipher = encrypt(plaintext, key_matrix, key_matrix_two, size)
	print(cipher)
	cipher = list(reversed(cipher))
	print(cipher)
	ciphertext = encrypt(cipher, key_matrix, key_matrix_two, size)
	print(ciphertext)
	stop = time.process_time()
	x = 0
	ciphertext_chr = [0]*len(ciphertext)
	for i in ciphertext:
		ciphertext_chr[x] = chr(i)
		x = x+1
	ciphertext_chr = ''.join(ciphertext_chr)
	encryption_time = stop-start
	#new_plain = change_bit(plaintext)
	#cipher_alt = encrypt(new_plain, key_matrix, key_matrix_two, size)
	#cipher_alt = list(reversed(cipher_alt))
	#cipher_altered = encrypt(cipher_alt, key_matrix, key_matrix_two, size)
	#avalanche = get_difference(ciphertext,cipher_altered,plaintext_size)
	#print("Original: "+plaintext)
	#print("Altered: "+new_plain)
	#print((avalanche))
	#print("Data length: "+str(len(plaintext)))
	#print("Seconds to encrypt: "+str(encryption_time))
	
	start = time.process_time()
	plain_one = decrypt(ciphertext,key_matrix, key_matrix_two, size)
	print(plain_one)
	plain_one = list(reversed(plain_one))
	print(plain_one)
	plain = decrypt(plain_one, key_matrix, key_matrix_two, size)
	print(plain)
	stop = time.process_time()
	x = 0
	plaint = [0]*len(plain)
	for i in plain:
		plaint[x] = chr(i)
		x = x+1
	plaint = ''.join(plaint)
	print(plaint)
	if plaint == plaintext:
		print("Success")
	else:
		print("Fail")
	decryption_time = stop-start
	#print(plain)
	#plaintext = ''.join(plain).decode('utf-8')
	#print("Seconds to decrypt: "+str(decryption_time))
	#print("Decoded plaintext: ")
	#print(plaintext)
	#print(str(plaintext_size)+" "+str(key_generation_time)+" "+str(encryption_time)+" "+str(decryption_time))
iterations = range(1)
for i in iterations:
	main()
