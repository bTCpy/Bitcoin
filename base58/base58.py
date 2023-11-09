#Base58 encoding scheme based on the explanation on https://en.bitcoin.it/wiki/Base58Check_encoding
import hashlib

code_string = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def base58encode(data: bytes) -> str:
  x = int.from_bytes(data, 'big')
  output_string = []
  while(x > 0):
    x, i = divmod(x,58)
    output_string.append(code_string[i])

  num_leading_zeros = len(data) - len(data.lstrip(b'\x00'))
  res = num_leading_zeros * code_string[0] + ''.join(reversed(output_string))
  return res


#Test based on https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki Test vector 2 Chain m/0 ext pub
test2 = 'xpub69H7F5d8KSRgmmdJg2KhpAK8SR3DjMwAdkxj3ZuxV27CprR9LgpeyGmXUbC6wb7ERfvrnKZjXoUmmDznezpbZb7ap6r1D3tgFxHmwMkQTPH'

version = '0488b21e' # private = 0x0488ade4 (xprv), public = 0x0488b21e (xpub)
depth = '01'
fingerprint = 'bd16bee5'
childnumber ='00000000'
chain_code = 'f0909affaa7ee7abe5dd4e100598d4dc53cd709d5a5c2cac40e7412f232f7c9c'
key = '02fc9e5af0ac8d9b3cecfe2a888e2117ba3d089d8585886c9c826b6b22a98d12ea'

serialized = version + depth + fingerprint + childnumber + chain_code + key
checksum = hashlib.sha256(hashlib.sha256(bytes.fromhex(serialized)).digest()).digest().hex()
checksum = bytes.fromhex(checksum)[:4]

extended_public_key = base58encode(bytes.fromhex(serialized) + checksum)
print(extended_public_key)

if test2 == extended_public_key:
  print('Base58 encoding worked!)

