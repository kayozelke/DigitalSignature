from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
import argparse

## ARGUMENTY ##

parser = argparse.ArgumentParser()
parser.add_argument("-filePath", help="Path to your file", required=True)
args = parser.parse_args()
print("Given filePath:", args.filePath)

try:
    with open(args.filePath, "rb") as f:
        file = f.read()
except:
    print("An error occured. Cannot read file: " + args.filePath)
    exit(1)

# Make SHA
sha_content = SHA256.new()
sha_content.update(file)


try:
    # Open signature file
    with open("shared_sign/shared_signature.txt") as f:
        signature = f.read()
        signature = bytes.fromhex(signature)
except:
    print("An error occured. Cannot read signature file!")
    exit(1)



try:
    # Import public key
    with open("keys/public_key.pem") as f:
        public_key = RSA.importKey(f.read())
        
    # Verification
    verifier = PKCS1_v1_5.new(public_key)
    
except:
    print("An error occured. Cannot get public key!")
    exit(1)
    


# Exit code
if verifier.verify(sha_content, signature):
    print("Files match. Signature verified successfully.")
    exit(0)
else:
    print("Error: Could not verify!")
    exit(1)