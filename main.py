import RPi.GPIO as GPIO
import time,datetime,configparser,picamera,requests,os

config = configparser.ConfigParser()
config.read_file(open('config_fichier.cfg'))


data = configparser.ConfigParser()
data.read_file(open('data_fichier.cfg'))

class info_systeme():
    
    nom_section_photo  = 'PHOTO'
    nom_section_defaut = 'DEFAUT'
    nom_section_GSM =    'GSM'
    nom_date =           'date'
    nom_photo_total =    'nombre_photo_total'
    nom_photo_jour =     'nombre_photo_jour'
    nom_sms_total=       'nombre_sms_total'
    nom_sms_jour =       'nombre_sms_jour'
    nom_largeur =        'largeur_photo'
    nom_longueur =       'longueur_photo'
    nom_frames =         'frame'
    nom_email =          'email'
    nom_password =       'mot_de_passe'
    nom_telephone =      'telephone'
    
    def __init__(self):
        self.get_date()
        
    # Ecriture dans les fichiers date et config       
    def ecrire_data(self,section,nom,val):
        val = str(val)
        data.set(section,nom,val)
        with open('data_fichier.cfg', 'w') as config_fichier:
            data.write(config_fichier)
    
    def ecrire_config_date(self,nom,val):
        data.set(self.nom_section_defaut,nom,val)
        val = str(val)
        with open('data_fichier.cfg', 'w') as config_fichier:
            data.write(config_fichier)
            
    # Lecture et écriture de la date dans le fichier config
    def get_date(self):
        self.date_config = data.get(self.nom_section_defaut, self.nom_date)
        self.date_systeme = str(datetime.date.today())
    
    def set_date(self):
        self.get_date()
        #RAZ si nous changeons de jour
        if (self.date_systeme != self.date_config):
            
            self.date_config = self.date_systeme
            self.ecrire_data(self.nom_photo_jour,0)
            self.ecrire_data(self.nom_sms_jour,0)
            self.ecrire_config_date(self.nom_date,self.date_config)
            
# Class Photo :
# Elle hérite de la class info_systeme
# Elle gére tous les valeurs qui sont en liens avec les photo
class Photo(info_systeme):
    
    def __init__(self):
        self.get_frames()
        self.get_dimensions()
        self.get_valeur()
        
    def get_valeur(self):
        self.val_photo_total = data.getint(self.nom_section_photo, self.nom_photo_total)
        self.val_photo_jour  = data.getint(self.nom_section_photo, self.nom_photo_jour)
    
    def get_frames(self):
        self.frames = config.getint(self.nom_section_photo, self.nom_frames)
    
    def get_dimensions(self):
        self.largeur  = config.getint(self.nom_section_photo, self.nom_largeur)
        self.longueur = config.getint(self.nom_section_photo, self.nom_longueur)
    
    def nom_image(self):
        frame = 0
        while frame < self.frames:
            yield 'Images/image-%s-%02d.jpg' % (time.strftime("%Y%m%d-%H%M%S"),frame)
            frame += 1
            
# Class Photo :
# Elle hérite de la class info_systeme
# Elle gére tous les valeurs qui sont en liens avec les SMS                 
class Sms(info_systeme):
    
    def __init__(self):
        self.get_id()
        self.get_password()
        self.get_telephone()
        self.get_sms()
    #Lecture dans le fichier config l'id de connection. Ici l'id est une adresse mail
    def get_id(self):
        self.id_user = config.get(self.nom_section_defaut, self.nom_email)
        
    #Lecture dans le fichier config du mot de passe de connection   
    def get_password(self):
        self.password_user = config.get(self.nom_section_defaut, self.nom_password)
     
    #Lecture dans le fichier config du numéro de téléphone
    def get_telephone(self):
        self.telephone_user = config.get(self.nom_section_defaut, self.nom_telephone)
    
    #Lecture dans le fichier data du nombres sms envoyés
    def get_sms(self):
        self.val_sms_total = data.getint(self.nom_section_GSM, self.nom_sms_total)
        self.val_sms_jour  = data.getint(self.nom_section_GSM, self.nom_sms_jour)
      
        
def photo_mov(capteur):
    
    exec(open('photo.py').read())
    modif = Photo()
    modif.set_date();
    modif.ecrire_data(modif.nom_section_photo,modif.nom_photo_total,modif.val_photo_total+1)
    modif.ecrire_data(modif.nom_section_photo,modif.nom_photo_jour,modif.val_photo_jour+1)
    time.sleep(1)
    
    exec(open('sms.py').read())
    modif = Sms()
    modif.set_date();
    modif.ecrire_data(modif.nom_section_GSM,modif.nom_sms_total,modif.val_sms_total+1)
    modif.ecrire_data(modif.nom_section_GSM,modif.nom_sms_jour,modif.val_sms_jour+1)   
    time.sleep(1)
    print("Okay")
    
def main():
    #GPIO
    
    GPIO.setmode(GPIO.BCM)
    capteur=7
    GPIO.setup(capteur, GPIO.IN)
    GPIO.add_event_detect(capteur, GPIO.RISING, callback=photo_mov, bouncetime=50)
    while True:
        time.sleep(0.2) 
if __name__=='__main__':
    main()
    
    
