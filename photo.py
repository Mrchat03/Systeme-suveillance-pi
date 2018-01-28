import time
import picamera
import configparser

config = configparser.ConfigParser()
config.read_file(open('config_fichier.cfg'))

class Photo():
    
    nom_section_photo = 'PHOTO'
    nom_photo_total = 'nombre_photo_total'
    
    def __init__(self):
        self.nom = self.nom_photo_total;
        self.get_valeur();
    
    def get_valeur(self):
        self.val = config.getint(self.nom_section_photo,self.nom);
    
    def ecrire_config(self):      
        self.val += 1;
        self.val = str(self.val)
        config.set(self.nom_section_photo,self.nom,self.val)
        with open('config_fichier.cfg', 'w') as config_fichier:
            config.write(config_fichier)
            
class Photo_jour(Photo):
    
    nom_largeur = 'largeur_photo'
    nom_longueur = 'longueur_photo'
    nom_frames = 'frame'
    nom_photo_jour = 'nombre_photo_jour'
    
    def __init__(self):
        self.nom = self.nom_photo_jour;
        self.get_valeur();
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
            
photo_total = Photo()
photo_jour = Photo_jour()


with picamera.PiCamera() as camera:
    camera.resolution = (photo_jour.longueur,photo_jour.largeur)
    camera.framerate = 30
    camera.start_preview()
    # Temporisation
    time.sleep(1)
    start = time.time()
    camera.capture_sequence(photo_jour.nom_image(), use_video_port=True)
    finish = time.time()
    photo_total.ecrire_config()
    photo_jour.ecrire_config()

    

