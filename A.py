
from cryptography.hazmat.primitives.asymmetric import rsa
import sympy
from cryptography.hazmat.primitives import serialization
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import requests
import argparse



def find_prime_numbers(filename):
    with open(filename, 'r') as file:
        bits = file.read().strip()
        length = len(bits)
        
        p = None
        q = None

        # Liczby p i q są odnajdowane przez przeszukiwanie zawartości "trng_numbers.txt".
        # Liczba p jest przeszukiwana co bit dla wyrazu 512-bitowego od początku pliku
        # Liczba q jest przeszukiwana co bit dla wyrazu 512-bitowego od konca pliku
        # jesli spelniaja warunki, mogą być użyte
        
        # Iteracja od początku pliku
        for i in range(length - 512 + 1):
            binary_str = bits[i:i+512]
            decimal_num = int(binary_str, 2)
            #print(decimal_num)
            if sympy.isprime(decimal_num) and decimal_num > 0:
                p = decimal_num
                break
        
        # Iteracja od końca pliku
        for i in range(length - 1, 512 - 1, -1):
            binary_str = bits[i-512+1:i+1]
            decimal_num = int(binary_str, 2)
            if sympy.isprime(decimal_num) and decimal_num > 0:
                if p is None:
                    p = decimal_num
                else:
                    q = decimal_num
                    break
        
        return p, q

def calculate_d(e, f_n):
    def extended_gcd(a, b):
        if b == 0:
            return a, 1, 0
        else:
            d, x, y = extended_gcd(b, a % b)
            return d, y, x - (a // b) * y

    _, d, _ = extended_gcd(e, f_n)
    return d % f_n

## ARGUMENTY ##


parser = argparse.ArgumentParser()
parser.add_argument("-filePath", help="Path to your file", required=True)
args = parser.parse_args()
print("Given filePath:", args.filePath)


## POBRANIE TRNG ##

url_generate = 'http://instaqram.pl/'
url_file = 'http://instaqram.pl/final_trn.txt'

requests.get(url_generate)

# Pobierz zawartość pliku
response = requests.get(url_file)
content = response.text

# Zapisz zawartość do pliku
with open('trng/trng_numbers.txt', 'w') as file:
    file.write(content)

with open("trng/trng_numbers.txt", "r") as file:
    random_string = file.read().strip()








## OBLICZENIE KLUCZY ##

# https://justcryptography.com/rsa-key-pairs/

filename = 'trng/trng_numbers.txt'
p, q = find_prime_numbers(filename)

#print(sympy.isprime(p), sympy.isprime(q))


n = p * q
f_n = (p-1) * (q - 1)


#e = 7
e = 65537


d = calculate_d(e,f_n)

#print("n:   ", n)
#print("f_n: ", f_n)
#print("e:   ", e)
#print("d:   ", d)



private_key = rsa.RSAPrivateNumbers(
    p=p,
    q=q,
    d=d,
    dmp1=d % (p - 1),
    dmq1=d % (q - 1),
    iqmp=rsa.rsa_crt_iqmp(p, q),
    public_numbers=rsa.RSAPublicNumbers(e=e, n=n)
).private_key()

public_key = rsa.RSAPublicNumbers(
    e=e,
    n=n,
).public_key()

# Convert private_key to PEM format
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Convert public_key to PEM format
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Write keys to file
with open('./keys/private_key.pem', 'wb') as f:
    f.write(private_pem)

with open('./keys/public_key.pem', 'wb') as f:
    f.write(public_pem)





# HASHOWANIE I SZYFROWANIE #


with open(args.filePath, "rb") as f:
    file = f.read()

# Import private key
with open("keys/private_key.pem", "r") as myfile:
    private_key = RSA.importKey(myfile.read())

# Make SHA
sha_content = SHA256.new()
sha_content.update(file)


# Create siganture
signer = PKCS1_v1_5.new(private_key)
signature = signer.sign(sha_content)

# Save siganture
with open("shared_file/shared_signature.txt", "w") as file:
    file.write(signature.hex())

    print("Signature created! Path: sharedfile/shared_signature.txt")