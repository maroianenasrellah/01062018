######################################################################################################################
def barcode_scan():
    # initialize the video stream and allow the camera sensor to warm up
    print("[INFO] starting video stream...")
    vs = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)

    barcodeData=""
    try:
        while True:
            frame = vs.read()
            barcodes = pyzbar.decode(frame)
            for barcode in barcodes:
                barcodeData = barcode.data.decode("utf-8")
                barcodeDatahex = barcodeData.encode('utf-8')
                print("Scanned Barcode Data",barcodeData)
                print("Data en Hex : ",barcodeDatahex.hex())
##                    if(barcodeData != oldbData):
##                        oldbData=barcodeData
##                        print("Scanned Barcode Data",barcodeData)
##                     
    except KeyboardInterrupt:
        print("[INFO] cleaning up...")
        vs.stop()