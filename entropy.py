import math


def entropy(string):
    "Calculates the Shannon entropy of a string"

    # get probability of chars in string
    prob = [ float(string.count(c)) / len(string) for c in dict.fromkeys(list(string)) ]

    # calculate the entropy
    entropy = - sum([ p * math.log(p) / math.log(2.0) for p in prob ])

    return entropy


def entropy_ideal(length):
    "Calculates the ideal Shannon entropy of a string with given length"

    prob = 1.0 / length

    return -1.0 * length * prob * math.log(prob) / math.log(2.0)

ciphertext =[151, 174, 40, 240, 168, 170, 115, 132, 129, 38, 26, 159, 189, 194, 62, 180, 16, 218, 2, 107, 245, 170, 103, 110, 79, 246, 186, 23, 21, 128, 83, 122, 88, 33, 127, 31, 121, 59, 20, 248, 24, 226, 115, 76, 158, 164, 177, 208, 181, 186, 223, 236, 142, 194, 131, 66, 111, 21, 131, 48, 194, 37, 83, 44, 60, 10, 129, 85, 24, 158, 111, 59, 180, 44, 235, 202, 145, 222, 163, 89, 208, 160, 157, 164, 164, 96, 9, 9, 57, 173, 124, 143, 84, 82, 196, 125, 15, 97, 90, 169, 56, 252, 19, 238, 38, 19, 32, 142, 102, 192, 47, 81, 101, 170, 154, 133, 105, 240, 60, 89, 3, 10, 9]

ciphertext_chr = [None]*len(ciphertext)
x = 0
print(len(ciphertext_chr))
for i in ciphertext:
	ciphertext_chr[x] = chr(i)
	x = x+1
cipher = ''.join(ciphertext_chr)
print(cipher)

entropyIs = entropy(cipher)
print("Current entropy: "+str(entropyIs))

ideal = entropy_ideal(len(cipher))
print("Ideal entropy is: "+str(ideal))