import configparser,picamera,time

def main(): 
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

if __name__=='__main__':
    main()
