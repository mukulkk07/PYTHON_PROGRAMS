import random
import string
chars=" "+string.punctuation+string.digits+string.ascii_letters
chars=list(chars)
key=chars.copy()
random.shuffle(key)
print(f"chars={chars}")
print(f"key={key}")
#ENCRYPTING
plain=input("Enter your message: ")
cypher=""

for letter in plain:
    index=chars.index(letter)
    cypher+=key[index]

print(f"original message={plain}")
print(f"cyphered message={cypher}")
