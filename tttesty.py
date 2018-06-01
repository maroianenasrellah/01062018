import MySQLdb



def qr_passage(code, date_heure, synchro):
    try:
        db = MySQLdb.connect("127.0.0.1", "yapo", "pipi", "rpi")
        curs=db.cursor()
        query="INSERT INTO rpi.QR_Code SET Code='%s', Dh_Lecture='%s', Est_synchro_O_N='%s'" % (code, date_heure, synchro)
        curs.execute(query)
        print("log a bien été ajouté !'")
        db.commit()
        db.close()
    except MySQLdb.Error as err:
        print("Exception while MYSQL Connection")
        print(err)
        db.close()
##        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
##            print("Something is wrong with your user name or password")
##            db.close()
##        elif err.errno == errorcode.ER_BAD_DB_ERROR:
##            print("Database does not exist")
##            db.close()
##        else:
##            print(err)
##            db.close()

c=1
date_h="20180524"
syn='NO'
qr_passage(c, date_h, syn)