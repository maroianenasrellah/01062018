import pyqrcode
import hashlib

big_qrcode=pyqrcode.create('MGR_20180530-500.1234xx')
big_qrcode.png('codeMGR.png', scale=5)
big_qrcode.show()
    


