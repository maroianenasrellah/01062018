import pyqrcode
import hashlib
import binascii
import datetime

debug=False
stoday = datetime.datetime.today()
DATE_TODAY=stoday.strftime("%Y%m%d")

X1=(10).to_bytes(2, byteorder='big')
m=hashlib.md5(X1)

X2=(24).to_bytes(2, byteorder='big')
m2=hashlib.sha256(X2)

print("digest size",m.digest_size)
#code =b"MGR_"+ DATE_TODAY.encode() +b"-500.1234"+
print(X1+X2)
##print(m.digest())
##print(m.hexdigest())
##
##print(m2.digest())
##print(m2.hexdigest())

if debug == True:
    
    #################################
    m=hashlib.md5(code)
    m.digest()
    m.hexdigest()
    #################################
    print("########### MD5 hash ##############\n")
    print("mdigest",m.digest())
    print("mhexdigest",m.hexdigest())
    print("digest size",m.digest_size)
    print("Block size ",m.block_size)
    print("\n")
    #################################
    h=hashlib.sha256(code)
    h.digest()
    h.hexdigest()
    #################################
    print("########### SHA256 HASH ###########\n")
    print("hdigest",h.digest())
    print("hhexdigest",h.hexdigest())
    print("digest size",m.digest_size)
    print("Block size ",m.block_size)

##dk=hashlib.pbkdf2_hmac('sha256',b'password',b'salt',100000)
##d=binascii.hexlify(dk)
##print(d)
    big_qrcode=pyqrcode.create(code)
    big_qrcode.png('codeMGR.png', scale=5)
    big_qrcode.show()