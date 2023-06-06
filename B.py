from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
import argparse

## ARGUMENTY ##

parser = argparse.ArgumentParser()
parser.add_argument("-filePath", help="Path to your file", required=True)
args = parser.parse_args()
print("Given filePath:", args.filePath)

with open(args.filePath, "rb") as f:
    file = f.read()

# Make SHA
sha_content = SHA256.new()
sha_content.update(file)

# Open signature file
with open("shared_file/shared_signature.txt") as f:
    signature = f.read()
    signature = bytes.fromhex(signature)

# Import public key
with open("keys/public_key.pem") as f:
    public_key = RSA.importKey(f.read())

# Verification
verifier = PKCS1_v1_5.new(public_key)

# Exit code
if verifier.verify(sha_content, signature):
    print("Files match!")
    exit(0)
else:
    print("Error: Could not verify!")
    exit(1)