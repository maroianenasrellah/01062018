#hash code
import hashlib
mystring = "whatever your string is"

m = hashlib.md5(mystring.encode('utf-8'))
print(m.hexdigest())
