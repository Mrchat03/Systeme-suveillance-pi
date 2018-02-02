import RPi.GPIO as GPIO
import time,datetime,configparser

config = configparser.ConfigParser()
config.read_file(open('config_fichier.cfg'))

class info_systeme():
    
    nom_section_photo = 'PHOTO'
    nom_section_defaut = 'DEFAUT'
    nom_date = 'date'
    nom_photo_total = 'nombre_photo_total'
    nom_photo_jour = 'nombre_photo_jour'
    nom_largeur = 'largeur_photo'
    nom_longueur = 'longueur_photo'
    nom_frames = 'frame'
    
    def get_valeur(self):
        self.val_photo_total = config.getint(self.nom_section_photo,self.nom_photo_total)
        self.val_photo_jour = config.getint(self.nom_section_photo,self.nom_photo_jour)
        
    def ecrire_config_photo(self,nom,val):
        val += 1;
        val = str(val)
        config.set(self.nom_section_photo,nom,val)
        with open('config_fichier.cfg', 'w') as config_fichier:
            config.write(config_fichier)
    
    def ecrire_config_date(self,nom,val):
        config.set(self.nom_section_defaut,nom,val)
        val = str(val)
        with open('config_fichier.cfg', 'w') as config_fichier:
            config.write(config_fichier)
            
class Photo(info_systeme):
    
    def __init__(self):
        self.get_frames();
        self.get_dimensions();
    
    def get_frames(self):
        self.frames = config.getint(self.nom_section_photo,self.nom_frames)
    
    def get_dimensions(self):
        self.largeur = config.getint(self.nom_section_photo,self.nom_largeur)
        self.longueur = config.getint(self.nom_section_photo,self.nom_longueur)
    
    def nom_image(self):
        frame = 0
        while frame < self.frames:
            yield 'Images/image%02d.jpg' % frame
            frame += 1
    
class Date(info_systeme):
    
    def get_date(self):
        self.date_config = config.get(self.nom_section_defaut ,self.nom_date)
        self.date_systeme = str(datetime.date.today())
    
    def set_date(self):
        self.get_date()
        if (self.date_systeme != self.date_config):
            self.date_config = self.date_systeme
            self.val_photo_jour = 0
            self.ecrire_config_photo(self.nom_photo_jour,self.val_photo_jour)
            self.ecrire_config_date(self.nom_date,self.date_config)
    
def photo_mov():
    
    exec(open('photo.py').read())
    modif = Date()
    modif.set_date();
    modif.get_date();
    modif.get_valeur();
    modif.ecrire_config_photo(modif.nom_photo_total,modif.val_photo_total)
    modif.ecrire_config_photo(modif.nom_photo_jour,modif.val_photo_jour)
    time.sleep(1)
    
def main():
    #GPIO
    GPIO.setmode(GPIO.BOARD)
    capteur=7
    GPIO.setup(capteur, GPIO.IN)
    while True:
      if GPIO.input(capteur):
            photo_mov()
        
if __name__=='__main__':
    main()
    
    
