import pygame
import pygame.camera
import mss.tools

def save():

    pygame.camera.init()

    imgs = []

    for _ in pygame.camera.list_cameras():

        cam = pygame.camera.Camera(_, (640, 480))
        cam.start()

        img = cam.get_image()
        imgs.append(mss.tools.to_png(pygame.image.tostring(img, 'RGB'), (640, 480)))

        cam.stop()

    return(imgs)
