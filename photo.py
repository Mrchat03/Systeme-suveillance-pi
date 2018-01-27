import time
import picamera
import os
import configparser

config = configparser.ConfigParser()
config.read_file(open('config_fichier.cfg'))

class Photo:
    def __init__(self,section,nom):
        self.section =section;
        self.nom = nom;
        self.get_valeur();
    
    def get_valeur(self):
        self.val = config.getint(self.section,self.nom);
    
    def ecrire_config(self):      
        self.val += 1;
        self.val = str(self.val)
        config.set(self.section,self.nom,self.val)
        with open('config_fichier.cfg', 'w') as config_fichier:
            config.write(config_fichier)
            
    def nom_image(self):
        frame = 0
        while frame < frames:
            yield 'Images/image%02d.jpg' % frame
            frame += 1
                 
photo_total = Photo('PHOTO','nombre_photo_total')
photo_jour = Photo('PHOTO','nombre_photo_jour')
frames = config.getint('PHOTO','frame')
largeur = config.getint('PHOTO','largeur_photo')
longueur = config.getint('PHOTO','longueur_photo')

with picamera.PiCamera() as camera:
    camera.resolution = (longueur,largeur)
    camera.framerate = 30
    camera.start_preview()
    # Temporisation
    time.sleep(0.2)
    start = time.time()
    camera.capture_sequence(photo_jour.nom_image(), use_video_port=True)
    finish = time.time()
    photo_total.ecrire_config()
    photo_jour.ecrire_config()

    
