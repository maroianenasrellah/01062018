#!/usr/bin/python
#-*- coding: utf-8 -*-
from datetime import datetime
import RPi.GPIO as GPIO
import MFRC522
import smbus
import time
import datetime
import hexdump
import MySQLdb

exec(open("/home/pi/New/sushi.py").read())

#################################################VARIABLES#################################################
today = datetime.datetime.today() 
str_today =today.strftime("%Y%m%d")
DATE_TODAY= str_today

##print("Date du jour: ",DATE_TODAY[0]+DATE_TODAY[1]+DATE_TODAY[2]+DATE_TODAY[3]+"-"+DATE_TODAY[4]+DATE_TODAY[5]+"-"+DATE_TODAY[6]+DATE_TODAY[7])

# Datetime
#stoday = datetime.datetime.today()
    
##DATE_LAST_PASS
DATE_LAST_PASS = ""

##DATE_CARD_VALID
DATE_CARD_VALID = ""

#secteur 0
B0S2=2
##secteur1
B1S4=4
B1S5=5
B1S6=6
##secteur2
B2S8=8
B2S9=9
B2S10=10

##secteur3
B3S12=12
B3S13=13
B3S14=14

##caractéristique
CREDIT_TOTAL = 0
CONSO_JOUR = 0
CONSO_TOTAL = 0
NBR_SEAUX_MAX = 0
Solde=0
##LED
GPIO_LEDR = 36
GPIO_LEDV = 32

# relais
GPIO_relais = 40# le relais est branche sur la pin 40 / GPIO21
GPIO.setmode(GPIO.BOARD) # comme la librairie MFRC522
GPIO.setwarnings(False)
GPIO.setup(GPIO_relais, GPIO.OUT)# Define some device parameters
GPIO.setup(GPIO_LEDV, GPIO.OUT)
GPIO.setup(GPIO_LEDR, GPIO.OUT)
##GPIO_bouton = 19
##GPIO.setup(GPIO_bouton, GPIO.IN)

I2C_ADDR  = 0x3f
#I2C_ADDR  = 0x77# I2C device address, if any error, change this address to 0x3f
LCD_WIDTH = 16   # Maximum characters per line


#LCD 
# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

bus = smbus.SMBus(1)
lcd_init()
lcd_byte(0x01,LCD_CMD)

######################################################################################################################
# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()
i=0


# This loop checks for chips. If one is near it will get the UID
try:

	while True:
		# Display Message
		i=i+1
		stoday = datetime.datetime.today()
		lcd_string(stoday.strftime("%d-%m-%Y %H:%M"),LCD_LINE_1)
		lcd_string("Attente Carte",LCD_LINE_2)
		print("Attente Carte : ",i)
		# Scan for cards
		(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
		##GPIO.cleanup()
		
		# If a card is found
		if status == MIFAREReader.MI_OK:
			print ("Carte detectee")
		# Get the UID of the card
		(status,uid) = MIFAREReader.MFRC522_Anticoll()
		# If we have the UID, continue
		if status == MIFAREReader.MI_OK:
			#Print UID
			UID = str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])+","+str(uid[4])
			print("UID: "+UID)
			GCP_UID=str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])+str(uid[4])
			print("GCP_UID: "+GCP_UID)
			GCP_DATE_PASSAGE=stoday.strftime("%d%m%Y %H:%M:%S")
			print("GCP_DATE_PASSAGE: ",GCP_DATE_PASSAGE)
			#lcd_string(""+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]),LCD_LINE_2)
			# Attendre 2 secondes
			#time.sleep(1)
			
			# This is the private key for authentication
			keyA_Prive = [0x59,0x61,0x50,0x6F,0x54,0x74] #"YaPoTt"
			
			# Select the scanned tag
			MIFAREReader.MFRC522_SelectTag(uid)
			
			# Authenticate with private key
			#print("..............................BLOC 0.....................................")
##			status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, B0S2,keyA_Prive, uid)
##			if(status == MIFAREReader.MI_OK):
##                            try:
##                                print("..............................BLOC 0.....................................")
##                                LicenseData = MIFAREReader.MFRC522_Read(B0S2)
##                                num_License=read_card(LicenseData)
##                                num_Licensetemp = num_License
##                            except:
##                                print("\nErreur Reading secteur ",B0S2,"\n")
                                                    
                               # print(num_Licensetemp)
			#print("..............................BLOC 1.....................................")
			status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, B1S4,keyA_Prive, uid)
			if(status == MIFAREReader.MI_OK):
				try:	
					print("..............................BLOC 1.....................................")
					#print("...................Authentification succeeded BLOC:",B1S4,"...................")
					nomData= MIFAREReader.MFRC522_Read(B1S4)
					nomtemp =read_card(nomData)
					print("NOM: ",nomtemp,"\n")
					prenomData = MIFAREReader.MFRC522_Read(B1S5)
					prenomtemp =read_card(prenomData)
					print("PRENOM: ",prenomtemp,"\n")
					societeData = MIFAREReader.MFRC522_Read(B1S6)
					societetemp =read_card(societeData)
					print("SOCIETE: ",societetemp,"\n")
					CARD = ""
					
				except:
					print("\nErreur Reading secteur ",B1S4,"\n")
			GCP_NOM=nomtemp
			GCP_PRENOM=prenomtemp
			GCP_CLUB=societetemp
		#	print("..............................BLOC 2.....................................")   
			status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, B2S8,keyA_Prive, uid)
			if(status == MIFAREReader.MI_OK):
				try:	
					print("..............................BLOC 2.....................................") 
					#print ("Authentification succeeded BLOC:",B2S8,"\n")
					backData = MIFAREReader.MFRC522_Read(B2S8)
					CARD=h2str(backData[0])
					DATE_CARD_VALID=recup_date_val(backData)
					CREDIT_TOTAL=int(backData[9])*256+int(backData[10])
					NBR_SEAUX_MAX = backData[11]
					GCP_CLIENT_CODE="yapo"
					
				except :
					print("\nErreur Reading secteur ",B2S8,"\n")
					
				GCP_CREDIT=CREDIT_TOTAL
				GCP_JOUR_MAX=NBR_SEAUX_MAX
				GCP_CARD_TYPE=CARD
				GCP_DATE_VALID=DATE_CARD_VALID
				print("..............................BLOC 3.....................................")
				status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, B3S12,  keyA_Prive, uid)
				if status == MIFAREReader.MI_OK:
					backData = MIFAREReader.MFRC522_Read(B3S12)
					#datetemp =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
					DATE_LAST_PASS=recup_date_val(backData)
					CONSO_TOTAL=(int(backData[9])*256+int(backData[10]))
					CONSO_JOUR = int(backData[11])
					
					GCP_CONSO=CONSO_TOTAL
					#GCP_DATE_PASSAGE=DATE_LAST_PASS
					
					if CARD == "A":
                                            #msg("BONJOUR MONSIEUR",nom)
                                            msg("BONJOUR MONSIEUR",nomtemp)
                                            time.sleep(1)
					
					
					if DATE_CARD_VALID >= DATE_TODAY:
						
						print("Votre carte est à jour\n")
						
						if(CREDIT_TOTAL > CONSO_TOTAL):
                                                    
                                                    if(DATE_TODAY > DATE_LAST_PASS):
                                                        DATE_LAST_PASS = DATE_TODAY
                                                        CONSO_JOUR = 0
                                                        GCP_JOUR_USED = CONSO_JOUR
                                                    if(DATE_TODAY == DATE_LAST_PASS):
                                                            
                                                            if(NBR_SEAUX_MAX > CONSO_JOUR):
								
								
                                                                    
                                                                    status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 12,keyA_Prive, uid)
                                                                
                                                                    if status == MIFAREReader.MI_OK:
                                                                        
                                                                            CONSO_JOUR = CONSO_JOUR+1
                                                                            CONSO_TOTAL = CONSO_TOTAL+1
                                                                            
                                                                            GCP_UID=str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])+str(uid[4])
                                                                            GCP_CONSO = CONSO_TOTAL
                                                                            GCP_JOUR_USED = CONSO_JOUR
                                                                            
                                                                            print("GCP_UID: ",GCP_UID,"\n")
                                                
                                                                            print("Type Card",GCP_CARD_TYPE,"\n")
                                                                            print("NOM: ",GCP_NOM,"\n")
                                                                            print("PRENOM: ",GCP_PRENOM,"\n")
                                                                            print("CLUB: ",GCP_CLUB,"\n")
                                                                            print("Date Limite De Validité: ",GCP_DATE_VALID,"\n")
                                                                            print("Date Dernier Passage: ",GCP_DATE_PASSAGE,"\n")
                                                                            print("Crédit Cumulé: ",GCP_CREDIT,"\n")
                                                                            print("Unités Consommées",GCP_CONSO,"\n")
                                                                            print("MAX seaux par jour: ",GCP_JOUR_MAX,"\n")
                                                                            print("Unités Consommées du jour:",GCP_JOUR_USED,"\n")
                                                                            print("Code CLIENT :",GCP_CLIENT_CODE,"\n")
                                                            
                                                                             ###insertion
                                                                            insert_passage(str(GCP_UID), GCP_CARD_TYPE, GCP_NOM,GCP_PRENOM,GCP_CLUB,GCP_DATE_VALID,GCP_DATE_PASSAGE,GCP_CREDIT,GCP_CONSO,GCP_JOUR_MAX,GCP_JOUR_USED,GCP_CLIENT_CODE)
                                                                           
                                                                            print("ECRITURE CARTE",CONSO_TOTAL)
                                                                            s = b"X" + DATE_TODAY.encode() + (CONSO_TOTAL).to_bytes(2, byteorder='big') + (CONSO_JOUR).to_bytes(1, byteorder='big') + b"YAPO"
                                                                            #print("s : ",hexdump.dump(s,sep=":"))
                                                                            MIFAREReader.MFRC522_Write(B3S12,s)
                                                                            
                                                                            ##MIFAREReader.MFRC522_StopCrypto1()
                                                                            # On allume la LED 
                                                                            GPIO.output(GPIO_LEDV,1)
                                                                            declencher_relais()
                                                                            Solde=(int(CREDIT_TOTAL)-int(CONSO_TOTAL))
                                                                            print("RECUPERER BALLES")
                                                                            
                                                                            #IMPORTANT à VOIR si CREDIT_TOTAL-CONSO_TOTAL =< NBR_SEAUX_MAX ALORS NBR_SEAUX_MAX = CREDIT_TOTAL-CONSO_TOTAL
                                                                            #EXPLICATION : SI NBR_SEAUX_MAX par jour  (10) et qu'il reste en CONSO_TOTAL que 8
                                                                            #il vaudrait mieux qu'il s'affiche 8/10 au lieu de 10/10 au premier passage du jour
                                                                            #Il faudra changer le nom de la variable NBR_SEAUX_MAX pour ne pas perturber les calculs du reste du code
                                                                            
                                                                            msg("CONSO JOUR:"+str(NBR_SEAUX_MAX-CONSO_JOUR)+"/"+str(NBR_SEAUX_MAX),"RECUPERER BALLES")
                                                                            time.sleep(2)
                                                                            msg("RESTE : "+str(CREDIT_TOTAL-CONSO_TOTAL)+"/"+str(CREDIT_TOTAL),"RECUPERER BALLES")
                                                                            time.sleep(2)
                                                                            GPIO.output(GPIO_LEDV,0)
                                                                            j= 10     
                                                                            while j > 0:
                                                                                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 12,keyA_Prive, uid)
                                                                                if status == MIFAREReader.MI_OK:
                                                                                    print(j-1,"seconde Reste")
                                                                                    print("veuillez retirer votre Carte")
                                                                                    msg("VEUILLEZ RETIRER","VOTRE CARTE")
                                                                                    j = j - 1
                                                                                    time.sleep(0.2)
                                                                                else:
                                                                                     j = -1
                                                                                     MIFAREReader.MFRC522_StopCrypto1()
                                                                                     print(" Carte retiré ")
                                                                                     ##msg("CARTE","RETIREE")
                                                                                    
                                                                                if j == 0:
                                                                                    MIFAREReader.MFRC522_StopCrypto1()
                                                                                    #time.sleep(2)
                                                                            
                                                                                         
                                                            if(NBR_SEAUX_MAX <= CONSO_JOUR):
                                                                    GCP_CONSO=CONSO_TOTAL
                                                                    GCP_JOUR_USED=CONSO_JOUR
                                                                    insert_passage(str(GCP_UID), GCP_CARD_TYPE, GCP_NOM,GCP_PRENOM,GCP_CLUB,GCP_DATE_VALID,GCP_DATE_PASSAGE,GCP_CREDIT,GCP_CONSO,GCP_JOUR_MAX,GCP_JOUR_USED,GCP_CLIENT_CODE)
                                                                    print("Nombre seaux authorise par jour atteint",CONSO_JOUR,"")
                                                                    GPIO.output(GPIO_LEDR,1)
                                                                    msg("MAX SEAUX JOURS","ATTEINT "+str(CONSO_JOUR)+"/"+str(NBR_SEAUX_MAX))
                                                                    ##turnOn(GPIO_LEDR,1)
                                                                    time.sleep(1)
                                                                    msg("CREDIT RESTANT","       "+str(CREDIT_TOTAL-CONSO_TOTAL)+"/"+str(CREDIT_TOTAL))
                                                                    time.sleep(1)
                                                                    msg("MAX SEAUX JOURS","ATTEINT "+str(CONSO_JOUR)+"/"+str(NBR_SEAUX_MAX))
                                                                    ##turnOn(GPIO_LEDR,1)
                                                                    time.sleep(1)
                                                                    msg("CREDIT RESTANT","       "+str(CREDIT_TOTAL-CONSO_TOTAL)+"/"+str(CREDIT_TOTAL))
                                                                    time.sleep(1)							
						if(CREDIT_TOTAL <= CONSO_TOTAL):
							insert_passage(str(GCP_UID), GCP_CARD_TYPE, GCP_NOM,GCP_PRENOM,GCP_CLUB,GCP_DATE_VALID,GCP_DATE_PASSAGE,GCP_CREDIT,GCP_CONSO,GCP_JOUR_MAX,GCP_JOUR_USED,GCP_CLIENT_CODE)
							print("Plus De Credit",CREDIT_TOTAL,"/",CONSO_TOTAL)
							msg("PLUS DE CREDIT ",str(CREDIT_TOTAL)+"/"+str(CONSO_TOTAL))
							GPIO.output(GPIO_LEDR,1)
							time.sleep(1.5)
							msg("RECHARGER CARTE",str(CREDIT_TOTAL)+"/"+str(CONSO_TOTAL))
							time.sleep(1.5)
					
					print("Solde : "+str(Solde))
					print("Reste total",CREDIT_TOTAL,"/",CONSO_TOTAL)
					print("CREDIT_TOTAL: ",int(CREDIT_TOTAL),"")
					print("MAX seaux: ",int(NBR_SEAUX_MAX),"")
					print("Date Du Jour: ",DATE_TODAY,"")
					print("Date Dernier Passage: ",DATE_LAST_PASS,"")
					print("Unités Consommées",int(CONSO_TOTAL),"")
					print("Unités Consommées du jour:",int(CONSO_JOUR),"")
					MIFAREReader.MFRC522_StopCrypto1()

                                 		
					if DATE_CARD_VALID < DATE_TODAY:
						insert_passage(str(GCP_UID), GCP_CARD_TYPE, GCP_NOM,GCP_PRENOM,GCP_CLUB,GCP_DATE_VALID,GCP_DATE_PASSAGE,GCP_CREDIT,GCP_CONSO,GCP_JOUR_MAX,GCP_JOUR_USED,GCP_CLIENT_CODE)
						DATE_expire=DATE_CARD_VALID[6]+DATE_CARD_VALID[7]+"-"+DATE_CARD_VALID[4]+DATE_CARD_VALID[5]+"-"+DATE_CARD_VALID[0]+DATE_CARD_VALID[1]+DATE_CARD_VALID[2]+DATE_CARD_VALID[3]
						GPIO.output(GPIO_LEDR,1)
						print("Carte ",CARD," Expire Date limite de validite",DATE_expire)
						
						msg("CARTE EXPIREE","      "+str(DATE_expire))
						time.sleep(1.5)
						msg("ADRESSEZ-VOUS","AU GUICHET")
						time.sleep(1.5)
						msg("CARTE EXPIREE","      "+str(DATE_expire))
						time.sleep(1.5)
						msg("ADRESSEZ-VOUS","AU GUICHET")
						time.sleep(1.5)

						##turnOn(GPIO_LEDR,2)
						MIFAREReader.MFRC522_StopCrypto1()
						
		time.sleep(0.5)
		GPIO.output(GPIO_LEDR,0)
except KeyboardInterrupt:
	lcd_string("MACHINE ARRETEE",LCD_LINE_1)
	lcd_string("ESSAYEZ + TARD",LCD_LINE_2)









