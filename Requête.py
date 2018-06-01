import MySQLdb
##Requête
##SELECT   COUNT(*) AS nbr_doublon, champ1, champ2, champ3
##FROM     table
##GROUP BY champ1, champ2, champ3
##HAVING   COUNT(*) > 1
##
##
##SELECT   COUNT(email) AS nbr_doublon, email
##FROM     utilisateur
##GROUP BY email
##HAVING   COUNT(email) > 1
def qr_passage():
    try:
        db = MySQLdb.connect("127.0.0.1", "yapo", "pipi", "rpi")
        curs=db.cursor()
        cod='a19178ff8738b2413bb356d32a3be42ep'
##        query = ("SELECT COUNT(*),Code,Dh_Lecture,Est_synchro_O_N FROM QR_Code "
##         "WHERE Code=%s")
        sql = "SELECT COUNT(*),Code,Dh_Lecture,Est_synchro_O_N FROM QR_Code WHERE Code='%s'" % (cod)
        
        curs.execute(sql)
        # Fetch all the rows in a list of lists.
        results = curs.fetchall()
       # print(results)
        for row in results:
            fcount = row[0]
            fcode = row[1]
            fdate = row[2]
            fsyn = row[3]
            
        # Now print fetched result
        print("Count=%s ,Code=%s,Date_heure=%s,Syn=%s" %(fcount, fcode,fdate,fsyn))
    except MySQLdb.Error as err:
        print("Exception while MYSQL Connection")
        print(err)
        db.close()
        

qr_passage()

