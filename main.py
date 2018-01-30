import RPi.GPIO as GPIO
import time
import configparser
import datetime 

config = configparser.ConfigParser()
config.read_file(open('config_fichier.cfg'))

#GPIO
GPIO.setmode(GPIO.BOARD)
capteur=7
GPIO.setup(capteur, GPIO.IN)

class info_systeme():
    
    def __init__(self):
        self.nom_section_photo = 'PHOTO'
        self.nom_section_defaut = 'DEFAUT'
        self.nom_date = 'date'
        self.nom_photo_total = 'nombre_photo_total'
        self.nom_photo_jour = 'nombre_photo_jour'
          
    def ecrire_config(self,val,nom):
        val += 1;
        val = str(val)
        config.set(self.nom_section_photo,nom,val)
        with open('config_fichier.cfg', 'w') as config_fichier:
            config.write(config_fichier)       
class photo(info_systeme):
    
    def get_valeur(self):
        self.val_photo_total = config.getint(self.nom_section_photo,self.nom_photo_total)
        self.val_photo_jour = config.getint(self.nom_section_photo,self.nom_photo_jour)
    
class date(info_systeme):
    
    def get_date(self):
    self.date_config = config.get(self.nom_section_defaut ,self.nom_date)
    self.date_systeme = str(datetime.date.today())
    
    def set_date(self):
    self.get_date()
    if (self.date_systeme != self.date_config):
        self.date_config = self.date_systeme
    modif.val_photo_jour = 0
    
def photo_mov():
    print ("Mouvement detecter") 
    exec(open('photo.py').read())
    modif.get_date();
    modif.get_valeur();
    modif.ecrire_config(modif.val_photo_total,modif.nom_photo_total)
    modif.ecrire_config(modif.val_photo_jour,modif.nom_photo_jour)
    time.sleep(2)

modif=info_systeme()
while True:    
    photo_mov()
    time.sleep(5)
    
    
    
