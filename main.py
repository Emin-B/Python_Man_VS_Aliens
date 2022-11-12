import pygame
import random

from pygame import *


LARGEUR_ECRAN = 800
HAUTEUR_ECRAN = 600

img_vaisseau = "C:\\Users\\Emin\\OneDrive\\Formation\\Jeu en python\\vaisseau.png"


class Enemmi(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemmi, self).__init__()
        self.surf = pygame.image.load("C:\\Users\\Emin\\OneDrive\\Formation\\Jeu en python\\ennemi.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                LARGEUR_ECRAN + 50,
                random.randint(0, HAUTEUR_ECRAN)
            )
        )
        self.speed = random.randint(5, 20)
    
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Vaisseau(pygame.sprite.Sprite):
    
    def __init__(self):
        super(Vaisseau, self).__init__()
        self.surf = pygame.image.load("C:\\Users\\Emin\\OneDrive\\Formation\\Jeu en python\\vaisseau.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
    
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_SPACE]:
            if len(le_missile.sprites()) < 1:
                missile = Missile(self.rect.center)
                all_sprite.add(missile)
                le_missile.add(missile)
        
               
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LARGEUR_ECRAN:
            self.rect.right = LARGEUR_ECRAN
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HAUTEUR_ECRAN:
            self.rect.bottom = HAUTEUR_ECRAN


class Missile(pygame.sprite.Sprite):
    def __init__(self, center_missile):
        super(Missile, self).__init__()
        self.surf = pygame.image.load("C:\\Users\\Emin\\OneDrive\\Formation\\Jeu en python\\missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = center_missile
        )
        son_missile.play()
        
    def update(self):
        self.rect.move_ip(15, 0)
        if self.rect.left > LARGEUR_ECRAN:
            self.kill()
    

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center_vaisseau):
        super(Explosion, self).__init__()
        
        self._compteur = 10
        self.surf = pygame.image.load("C:\\Users\\Emin\\OneDrive\\Formation\\Jeu en python\\explosion.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = center_vaisseau
        )
    
        son_explosion.play()
        
    def update(self):
        self._compteur = self._compteur - 1
        
        if self._compteur == 0:
            self.kill()


class Etoile(pygame.sprite.Sprite):
    def __init__(self):
        super(Etoile, self).__init__()
        self.surf = pygame.image.load("C:\\Users\\Emin\\OneDrive\\Formation\\Jeu en python\\etoile.png")
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                LARGEUR_ECRAN + 20,
                random.randint(0, HAUTEUR_ECRAN)
            )
        )
    
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

class Score(pygame.sprite.Sprite):
    def __init__(self):
        super(Score, self).__init__()
        self._scoreCourant = 0
        self._setText()
    
    def _setText(self):
        self.surf = police_score.render(
            'Score : ' + str(self._scoreCourant), False, (255, 255, 255))
        self.rect = self.surf.get_rect(
            center = (LARGEUR_ECRAN / 2, 15)
        )
        
    def update(self):
        self._setText()
        
    def increment(self, valeur):
        self._scoreCourant = self._scoreCourant + valeur
        
        

pygame.font.init()
police_score = pygame.font.SysFont('Comic Sans MS', 30)


pygame.mixer.init()
son_missile = pygame.mixer.Sound("C:\\Users\\Emin\\OneDrive\\Formation\\Jeu en python\\laser.ogg")
son_explosion = pygame.mixer.Sound("C:\\Users\\Emin\\OneDrive\\Formation\\Jeu en python\\explosion.ogg")



clock = pygame.time.Clock()   


pygame.init()
pygame.display.set_caption("Man VS Aliens !!!!")


ADD_ENEMY = pygame.USEREVENT + 1 
pygame.time.set_timer(ADD_ENEMY, 500)
ADD_STAR = pygame.USEREVENT +2
pygame.time.set_timer(ADD_STAR, 100)


ecran = pygame.display.set_mode([LARGEUR_ECRAN, HAUTEUR_ECRAN])




all_sprite = pygame.sprite.Group()
le_missile = pygame.sprite.Group()
enemys = pygame.sprite.Group()
les_explosions = pygame.sprite.Group()
les_etoiles = pygame.sprite.Group()


vaisseau = Vaisseau()
all_sprite.add(vaisseau)
score = Score()
all_sprite.add(score)

continuer = True
while continuer:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
        elif event.type == ADD_ENEMY:
            new_enemy = Enemmi()
            enemys.add(new_enemy)
            all_sprite.add(new_enemy)
        elif event.type == ADD_STAR:
            new_star = Etoile()
            les_etoiles.add(new_star)
            all_sprite.add(new_star)

    ecran.fill((0, 0, 0))
    
    if pygame.sprite.spritecollideany(vaisseau, enemys):
        vaisseau.kill()
        explosion = Explosion(vaisseau.rect.center)
        les_explosions.add(explosion)
        all_sprite.add(explosion)
        continuer = False
    
    
    for m in le_missile:
        liste_ennemis_touches = pygame.sprite.spritecollide(
            m, enemys, True)
        if len(liste_ennemis_touches) > 0:
            m.kill()
            score.increment(len(liste_ennemis_touches))
        for ennemi in liste_ennemis_touches:
            explosion = Explosion(ennemi.rect.center)
            les_explosions.add(explosion)
            all_sprite.add(explosion)
    
    touche_appuyee = pygame.key.get_pressed()
    
    vaisseau.update(touche_appuyee)
    le_missile.update()
    enemys.update()
    les_explosions.update()
    les_etoiles.update()
    score.update()
    
    for m in all_sprite:
        ecran.blit(m.surf, m.rect)

    pygame.display.flip()
    
    clock.tick(30)

pygame.time.delay(3000)

pygame.quit()


