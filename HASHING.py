import pyqrcode
import hashlib
import binascii
import datetime

XX=1024
stoday = datetime.datetime.today()
DATE_TODAY=stoday.strftime("%Y%m%d")

code =b'MGR_' + DATE_TODAY.encode() + b'-500.'+b'123'+(XX).to_bytes(2, byteorder='big')
#################################
m=hashlib.md5(code)
m.digest()
m.hexdigest()
##############################################
print("########### MD5 hash ##############\n")
print("mdigest",m.digest())
print("mhexdigest",m.hexdigest())
print("digest size",m.digest_size)
print("Block size ",m.block_size)
print("\n")
##############################################
h=hashlib.sha256(code)
h.digest()
h.hexdigest()
##############################################
print("########### SHA256 HASH ###########\n")
print("hdigest",h.digest())
print("hhexdigest",h.hexdigest())
print("digest size",m.digest_size)
print("Block size ",m.block_size)

##dk=hashlib.pbkdf2_hmac('sha256',b'password',b'salt',100000)
##d=binascii.hexlify(dk)
##print(d)