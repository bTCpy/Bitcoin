import os
import hashlib
import requests

def generate_entropy(bit_length):
  entropy = os.urandom(bit_length // 8) #Input needs to be in bytes
  entropy_bits = bin(int.from_bytes(entropy, byteorder = 'big'))[2:].zfill(len(entropy)*8) #convert bytes into bits
  return entropy_bits 

def create_checksum(entropy):
  entropy_hash = hashlib.sha256(entropy).digest()
  checksum_length = len(entropy) * 8 // 32 #Checksum (CS) = Initial entropy lenght (ENT)  / 32

  #Covert the hash into a binary string
  entropy_hash_binary = bin(int.from_bytes(entropy_hash, byteorder='big'))[2:].zfill(256)

  return entropy_hash_binary[:checksum_length]

def get_bip39_word_list():
  words = requests.get("https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt")
  
  if words.status_code == 200:
    text_data = words.text
    word_list = text_data.splitlines()
    return word_list
  
  else:
    wordlist_path = './wordlist_bip39/bip39_english_wordlist.txt'
    with open(wordlist_path, 'r') as file:
        word_list = file.read().splitlines()
    return word_list


bit_length = 128  #128 bits --> flipping a coin 128 times


#Step 1 Generating some Entropy using the generate_entropy function
entropy_bits = generate_entropy(bit_length)

#Step 2 Generate checksum (CS) by hashing with sha256 and calculating cs_length 
check_sum = create_checksum(entropy)

#Step 3 Append CS (bits) to initail entropy (in bits)
combined_bits = entropy_bits + check_sum

#Step 4 Download BIP-39 english wordlist and store in list

word_list = get_bip39_word_list()



