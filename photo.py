import time
import picamera
import configparser

config = configparser.ConfigParser()
config.read_file(open('config_fichier.cfg'))

class Photo():
    
    nom_section_photo = 'PHOTO'
    nom_largeur = 'largeur_photo'
    nom_longueur = 'longueur_photo'
    nom_frames = 'frame'
    
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
            
photo = Photo()

with picamera.PiCamera() as camera:
    camera.resolution = (photo.longueur,photo.largeur)
    camera.framerate = 30
    camera.start_preview()
    # Temporisation
    time.sleep(1)
    start = time.time()
    camera.capture_sequence(photo.nom_image(), use_video_port=True)
    finish = time.time()


    
