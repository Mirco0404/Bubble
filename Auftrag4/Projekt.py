import pygame                   # Stellt Objekte und Konstanten zur Spielprogrammierung zur Verfügung
import os
from random import randrange
import sys

#----------------------------------Einstellungen für das Spiel-------------------------------------------
class Settings(object):
    breite = 1500                                               #Breite des Fensters
    höhe = 800                                                  #Höhe des Fensters
    fps = 60                                                    #frames per second
    title = "Pop Bubble"                                        #Oben links angezeigter Titel Spiels bzw. Fensters
    file_path = os.path.dirname(os.path.abspath(__file__))      #Pfad angabe
    images_path = os.path.join(file_path, "images")             #Speicherort für die Bilder des Spiels
    sound_path = os.path.join(file_path, "sound")               #Speicherort für die Sounds des Spiels
    bordersize = 10                                             #Rand zu den Ecken des Fensters
    klick = False
    halten = False
    hover = False
    counter = 60
    Score = 0
    max_bubble = 0
    zeiteinheit = 60
    game_loos = False
    mouse_scale = (69, 75)
    mouse_mover = 30

#----------------------------------Definition zum schreiben des Highscores---------------------------------
def write_in_file(dir_name, file_name, text, overwrite):
    if overwrite:
        myFile = open(f'{Settings.file_path}/{dir_name}/{file_name}', 'w')  #Wenn überschrieben werden soll, wird die Datei high_score.txt bearbeitet mit dem Recht "write"
    else:
        myFile = open(f'{Settings.file_path}/{dir_name}/{file_name}', 'a')  #Es wird ein neuer Text unter den bereits vorhanden gesetzt, ohne dass der vorhandene ersetzt wird
    text = [text]                                                           #Wird in Text gespeichert

    for line in text:
        myFile.write(line)                                                  #Jedes Element in der obrigen Liste, wird in eine neue Zeile geschrieben

#----------------------------------Definition zum lesen des Highscores-------------------------------------
def value_out_of_file(dir_name, file_name):
    myFile = open(f'{Settings.file_path}/{dir_name}/{file_name}', 'r')      #Die Datei wird mit dem Recht "read" ausgelesen
    data = myFile.read()
    return data

#----------------------------------------------------------------------------------------------------------


#--------------------------------Klasse des Spielers--------------------------------
class Mouse(pygame.sprite.Sprite):
    def __init__(self, pygame):
        super().__init__()
        self.screen = pygame.display.set_mode((Settings.breite, Settings.höhe))
        self.image = pygame.image.load(os.path.join(Settings.images_path, "pin.png")).convert_alpha()     #Das Image wird in self.image gespeichert
        self.image = pygame.transform.scale(self.image, (69, 75))                                              #Das Image wird gescalet
        self.rect = self.image.get_rect()
        self.rect.x = Settings.breite // 2                                                               #X-Achsen Position wird auf die Breite des Fensters geteilt durch zwei gesetzt
        self.rect.y = Settings.höhe                                       #Y-Achsen Position wird auf die Höhe des Fensters minus bordersize_ground gesetzt.
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.left = pygame.mouse.get_pos()[0]                  #X-Koordinate der Maus
        self.rect.top = pygame.mouse.get_pos()[1]                   #Y-Koordinate der Maus
    
        if Settings.hover == True:                                                                                  #
            self.image = pygame.image.load(os.path.join(Settings.images_path, "pin2.png")).convert_alpha()          #
            self.image = pygame.transform.scale(self.image, (Settings.mouse_scale))                                 #Wenn über eine Bubble gehovert wir, ändert sich das Image des Maus
            self.rect.top -= Settings.mouse_mover                                                                   #
        else:
            self.image = pygame.image.load(os.path.join(Settings.images_path, "pin.png")).convert_alpha()           #
            self.image = pygame.transform.scale(game.Mouse.image, (Settings.mouse_scale))                           #Wenn über eine Bubble gehovert wird, setzt sich das Image zurück zum Standard

#----------------------------------------------------------------Bubble Klasse----------------------------------------------------------------
class Bubble(pygame.sprite.Sprite):
    def __init__(self, x , y):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 5                                                                                              #Radius der Bubble
        self.image = pygame.image.load(os.path.join(Settings.images_path, "current_bubble.png")).convert_alpha()     #Das Image wird in self.image gespeichert
        self.image = pygame.transform.scale(self.image, (self.radius * 2,self.radius * 2))                           #Das Image wird gescalet
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.timer = 0
        self.random_radius = randrange(1, 5)                                                                          #Random Radius bzw. Geschwindigkeit mit der die Bubbles wachsen
        Settings.max_bubble += 1                                                                                      #Maximale Anzahl an Bubbles wird erhöht

    def update(self):
        self.timer += 1
        if self.timer >= Settings.zeiteinheit:
            self.timer = 0
            self.radius += self.random_radius                                                                            #Die random generierte Zahl zwischen 1 und 4 aus self.random_radius wird für den Radius der Bubbles verwendet
            self.image = pygame.image.load(os.path.join(Settings.images_path, "current_bubble.png")).convert_alpha()     #Das Image wird in self.image gespeichert
            self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))                          #Das Image wird gescalet

            self.rect.left -= self.random_radius                                                                         #
            self.rect.top -= self.random_radius                                                                          #Hier werden die Ränder der Bubble korrekt mit geupdatet
            self.rect.width += self.random_radius * 2                                                                    #
            self.rect.height += self.random_radius * 2                                                                   #
        
        for bubble in game.all_Bubble:
            if bubble is self:                                  #Ohne diese Abfrage würde die Blase mit sich selbst kollidieren
                continue
            if pygame.sprite.collide_mask(self, bubble):        #Wenn eine Bubble mit einer anderen kollidiert...
                game.score_saver()                               #...wird die Funktion 'score_saver' aktiviert
                Settings.game_loos = True                       #Die Einstellung für game loos wird auf True gesetzt


        if self.rect.left <= 0:                                 #
            self.kill()                                         #
            Settings.max_bubble -= 1                            #
        if self.rect.top <= 0:                                  #Wenn eine Bubble auf einen der angegeben Ränder trifft, wird sie zerstört und die maximale Anzahl von Bubbles wird um eins gesänkt
            self.kill()                                         #
            Settings.max_bubble -= 1                            #
        if self.rect.right >= Settings.breite:                  #
            self.kill()                                         #
            Settings.max_bubble -= 1                            #
        if self.rect.bottom >= Settings.höhe:                   #
            self.kill()                                         #
            Settings.max_bubble -= 1                            #
#---------------------------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------Helfer für Maus-Bubble Kollision----------------------------------------------------------------
class Collision_helper(pygame.sprite.Sprite):
    def __init__(self, pygame):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(Settings.images_path, "black_circle.png")).convert_alpha()     #Das Image wird in self.image gespeichert
        self.image = pygame.transform.scale(self.image, (2, 2))                                                    #Das Image wird gescalet
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.centerx = pygame.mouse.get_pos()[0]                                                               #Der Collision_helper bekommt die X und Y Koordinaten der Maus und befindet sich oben links an der Spitze des Pins
        self.rect.centery = pygame.mouse.get_pos()[1]


#----------------------------------------------------------------Checkt den Abstand zu anderen Bubbles----------------------------------------------------------------
class bubble_kollision_helper(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.radius = 15                                                                                                        #Radius der Spawnbubble wird festgelegt
        self.image = pygame.image.load(os.path.join(Settings.images_path, "current_bubble.png")).convert_alpha()                #Das Image wird in self.image gespeichert
        self.image = pygame.transform.scale(self.image, (self.radius * 2,self.radius * 2))                                      #Das Image wird gescalet
        self.rect = self.image.get_rect()
        self.rect.centerx = randrange(0 + Settings.bordersize, Settings.breite - Settings.bordersize - self.radius)             #X-Koordiante der Spawnbubble
        self.rect.centery = randrange(0 + Settings.bordersize, Settings.höhe - Settings.bordersize - self.radius)               #Y-Koordiante der Spawnbubble

    def update(self):
        self.rect.centerx = randrange(0 + Settings.bordersize, Settings.breite - Settings.bordersize - self.radius)             #Geupdatete X-Koordiante der Spawnbubble
        self.rect.centery = randrange(0 + Settings.bordersize, Settings.höhe - Settings.bordersize - self.radius)               #Geupdatete Y-Koordiante der Spawnbubble


#--------------------------------Texte zum Anzeigen--------------------------------
class Text(object):
    def __init__(self, pygame):
        self.screen = pygame.display.set_mode((Settings.breite, Settings.höhe))                                                 #Der Screen wird festgelegt

        self.font = pygame.font.SysFont("comicsansms", 50)                                                                      #
        self.font2 = pygame.font.SysFont("comicsansms", 50)                                                                     #Formatierung der Texte welche angezeigt werden
        self.font3 = pygame.font.SysFont("comicsansms", 50)                                                                     #
    
    def rendering(self, text, x, y, font):
        if font:
            text = self.font2.render((text ), True, (138, 137, 131))                                                            #Wenn 'font' True ist, wird 'font2' gerendert
            self.screen.blit(text, (x , y))
        else:
            text = self.font.render((text ), True, (138, 137, 131))                                                             #Sonst wird 'font' gerendert
            self.screen.blit(text, (x , y))


#--------------------------------Allgemeine Game-Klasse--------------------------------

class Game(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((Settings.breite, Settings.höhe))                                                 #Der Screen wird festgelegt
        pygame.display.set_caption(Settings.title)

        self.brightness = pygame.Surface((Settings.breite, Settings.höhe))                                                      #
        self.brightness.fill((0, 0, 0))                                                                                         #Die Helligkeit wird in self.brightness gespeichert
        self.brightness.set_alpha(150)                                                                                          #
        
#----------------------------------------------------------------Festlegen des Backgrounds----------------------------------------------------------------
        self.background = pygame.image.load(os.path.join(Settings.images_path, "background.png")).convert()                     #
        self.background = pygame.transform.scale(self.background, (Settings.breite, Settings.höhe))                             #Der Hintergrund wird geladen und gescalet
        self.background_rect = self.background.get_rect()                                                                       #

#----------------------------------------------------------------Festlegen des Backgrounds----------------------------------------------------------------
        self.background_pause = pygame.image.load(os.path.join(Settings.images_path, "pause_screen.png")).convert()             #
        self.background_pause = pygame.transform.scale(self.background_pause, (Settings.breite, Settings.höhe))                 #Der Hintergrund wird geladen und gescalet
        self.background_pause_rect = self.background_pause.get_rect()                                                           #

#--------------------------------------------------------------------Variablen-----------------------------------------------------------------------------
        self.counter = 0                                                                                                        #Counter dafür, dass nach mindestens einer Sekunde eine Bubble gespawnt wird
        self.pause = False                                                                                                      #Variable ob Pause ist oder nicht                                                                                            #Variable für die Helligkeit des Spiels

#------------------------------------------------------------Gruppen und Objekte---------------------------------------------------------------------------
        self.all_Mouse = pygame.sprite.Group()                                                                                  #Hier wird die Gruppe der Maus erstellt
        self.Mouse = Mouse(pygame)                                                                                              #Maus Objekt wird erstellt
        self.all_Mouse.add(self.Mouse)                                                                                          #Maus Objekt wird der Gruppe hinzugefügt

        self.all_Collision = pygame.sprite.Group()                                                                              #Hier wird die Gruppe des Collision_helper erstellt
        self.Collision_helper = Collision_helper(pygame)                                                                        #Collision_helper Objekt wird erstellt
        self.all_Collision.add(self.Collision_helper)                                                                           #Collision_helper Objekt wird der Gruppe hinzugefügt

        self.all_Bubble = pygame.sprite.Group()                                                                                 #Hier wird die Gruppe der Bubble erstellt
        self.Bubble = Bubble(randrange(0 + Settings.bordersize, Settings.breite - Settings.bordersize), randrange(0 + Settings.bordersize, Settings.höhe - Settings.bordersize))#Bubble Objekt wird erstellt
        self.all_Bubble.add(self.Bubble)                                                                                        #Bubble Objekt wird der Gruppe hinzugefügt

        self.bubble_helper = bubble_kollision_helper()                                                                          #bubble_kollision_helper Objekt wird erstellt

        self.Text = Text(pygame)                                                                                                #Text Objekt wird erstellt

        self.clock = pygame.time.Clock()
        self.done = False
        pygame.mouse.set_visible(False)

#----------------------------------------------------------------Sound----------------------------------------------------------------
        #Background Music
        pygame.mixer.music.load(os.path.join(Settings.sound_path, "Remix2.mp3"))                                                #Hintergrund Musik wird geladen
        pygame.mixer.music.set_volume(.1)                                                                                       #Hintergrund Musik wird lesier gestellt
        pygame.mixer.music.play(loops=-1)                                                                                       #Hintergrund Musik wird im loop gespielt
        self.music_state = True

        #Sound effect
        self.blop = pygame.mixer.Sound('F:/Schule-2Jahr/Spieleprogrammierung-Adams/Auftrag4/sound/blop3.mp3')                   #Der Sound für das zerplätzen der Blasen wird in self.blop gespeichert
        self.spawn_sound = pygame.mixer.Sound('F:/Schule-2Jahr/Spieleprogrammierung-Adams/Auftrag4/sound/Jump20.wav')           #Der Sound für das spawnen der Blasen wird in self.spawn_sound gespeichert
        self.bubble_kollision = pygame.mixer.Sound('F:/Schule-2Jahr/Spieleprogrammierung-Adams/Auftrag4/sound/bubble_kollision.mp3')#Der Sound für Blasen Kollision wird in self.bubble_kollision gespeichert
        
        #Sound volume
        self.spawn_sound.set_volume(0.1)                                                                                        #Der Spawn-Sound wird leiser gestellt
        self.bubble_kollision.set_volume(0.2)                                                                                   #Der Kollisions-Sound der Bubbles wird leiser gestellt

#-------------------------------Kollision zwischen Maus und Bubble--------------------------------------
    def collision(self):
        if Settings.klick:                                                                                                      #Wenn geklickt wird...
            for bubbles in self.all_Bubble:                                                                                     #Werden zwei Listen mit den Inhalten der all_Bubble Gruppe erstellt
                for colli in self.all_Collision:                                                                                #
                    collision = pygame.sprite.collide_mask(bubbles, colli)                                                      #Kollisions Abfrage zwischen der bubbles und colli Liste
                    if bool(collision):                                                                                         #Wenn Maus und Bubble kollidieren...
                        self.blop.play()                                                                                        #Wird der blop-Sound abgespielt
                        bubbles.kill()                                                                                          #Die bubble gekillt
                        Settings.max_bubble -= 1                                                                                #Die maximale Anzahl an Bubbles wird um 1 reduziert
                        Settings.Score += game.Bubble.random_radius                                                             #Und dem oben links angezeigten Score, wird der random generierte Wachstumsradius der Bubble angerechnet
#--------------------------------------------------------------------------------------------------------

#------------------------------------------------run Funktion--------------------------------------------------------------#
    def run(self):
        while not self.done:                                                        #Hauptprogrammschleife mit Abbruchkriterium   
            self.clock.tick(Settings.fps)                                           #Setzt die Taktrate auf max 60fps   
            for event in pygame.event.get():                                        #Durchwandere alle aufgetretenen  Ereignisse
                if event.type == pygame.QUIT:                                       #Wenn das rechts oberen befindliche X im Fenster geklickt wird
                    self.score_saver()                                               #Wird der Score gesichert
                    self.done = True                                                #Und das Spiel beendet
                elif event.type == pygame.KEYDOWN:                                  #Event wird abgefragt, d.h. sobald "ESC" betätigt wird, schließt sich das Fenster und der Score wird gesichert.
                    if event.key == pygame.K_ESCAPE:                                #
                        self.score_saver()                                           #
                        self.done = True                                            #
                    if event.key == pygame.K_r:                                     #Wenn während des Spiels die Taste "R" betätigt wird, wird ein Befehl über die CMD gesendet, welcher das Spiel schließt und erneut öffnet.(Dient dem neustart)
                        os.execv(sys.executable, ['python'] + sys.argv)             #
                        sys.exit()                                                  #
                        
                elif event.type == pygame.KEYUP:                                    #Event wird abgefragt
                    if event.key == pygame.K_p:                                     #Wenn die Taste "P" betätigt wird...
                        if self.pause:                                              #Wenn self.pause False ist...
                            pygame.mixer.music.unpause()                            #Wird die Musik weiter laufen
                        else:                                                       #Wenn self.pause True ist
                            pygame.mixer.music.pause()                              #Wird die Musik pausiert
                            self.screen.blit(self.brightness, (0, 0))               #Das Bild wird dunkler
                            self.Text.rendering(f'Your Score: {Settings.Score}' , 600, 200, False)  #
                            self.Text.rendering('Game Paused' , 600, 300, False)                    #Diese Drei Texte erscheinen bzw. werden gerendert
                            self.Text.rendering('Press "R" to restart the game' , 400, 350, False)  #
                        self.pause = not self.pause                                 #Wenn "P" gedrückt wird, ändert sich der Status von self.pause


#---------------------------------------------------------------------------------------------------------------------------#
            if pygame.sprite.spritecollide(self.Collision_helper, self.all_Bubble, False):                                  #
                Settings.hover = True                                                                                       # Hier wird festgestellt, ob der Spieler über eine Bubble hovert
            else:                                                                                                           #
                Settings.hover = False                                                                                      #

            if pygame.mouse.get_pressed()[0] == True and Settings.klick == False and Settings.halten == False:              #
                Settings.klick = True                                                                                       # Hier wird festgestellt, ob der Spieler klickt
                Settings.halten = True                                                                                      #
            elif pygame.mouse.get_pressed()[0] == True and Settings.klick == True:                                          #
                Settings.klick = False                                                                                      #
                Settings.halten = True                                                                                      #
            elif pygame.mouse.get_pressed()[0] == False and Settings.halten == True:                                        #
                Settings.halten = False                                                                                     #
                Settings.klick = False                                                                                      #
#---------------------------------------------------------------------------------------------------------------------------#

#----------------------------------------------------Check ob das Game läuft-----------------------------------------------------------------------#
            if self.pause == False:                                                             #Wenn self.pause False ist
                self.screen.blit(self.background, self.background_rect)                         #Werden alle Funktionen ausgeführt, damit das Spiel läuft

                self.collision()
                self.all_Collision.update()

                self.all_Bubble.draw(self.screen)
                self.all_Bubble.update()

                self.all_Mouse.draw(self.screen)
                self.all_Mouse.update()

                self.draw_text()
                self.Collision_helper.update()

                if self.counter >= 60 and Settings.max_bubble < Settings.höhe * Settings.breite // 87500 - 1:   #Es wird abgefragt ob self.counter größer oder gleich 60 ist und ob max_bubble kleiner ist als der Wert welcher im Zusammenhang mit der Fenstergröße steht
                    self.bubble_helper.update()                                                                   #Das Objekt der bubble helper Klasse updatet sich
                    for self.Bubble in self.all_Bubble:                                                         #
                        if pygame.sprite.collide_circle(self.bubble_helper, self.Bubble):                         #Es wird geschaut, ob bubble helper und bubbe kollidieren
                            self.bubble_helper.update()                                                           #Wenn dies der Dall ist, wird die update Funktion erneut ausgeführt
                    self.spawn_sound.play()                                                                     #Wenn eine Bubble spawnt, wird der spawn_sound abgespielt
                    self.Bubble = Bubble(self.bubble_helper.rect.centerx, self.bubble_helper.rect.centery)          #Ein neues Obejekt wird erstellt
                    self.all_Bubble.add(self.Bubble)                                                            #Und der all_Bubble Gruppe hinzugefügt
                    self.counter = 0                                                                            #self.counter wird für den durchlauf wieder auf 0 gesetzt
                    print(Settings.Score)                                                                       #
                else:
                    self.counter += 1                                                                           #Sollte die erste obere if Abfrage nicht erfüllt sein, wird self.counter +1 gerechnet

                if Settings.zeiteinheit > 10:                                                                   #Solange Settings.Zeiteinheit größer als 10 ist...
                    Settings.zeiteinheit -= 0.01                                                                #Wird 60 mal in der Sekunde 0,01 abezogen, damit die Geschwindigkeit sich erhöht
#--------------------------------------------------------------------------------------------------------------------------------------------------#
            pygame.display.flip()   # Aktualisiert das Fenster


#----------------------------------------------------Rendert die angezeigten Texte-----------------------------------------------------------------------#
    def draw_text(self):
        score_save = value_out_of_file('score', 'high_score.txt')                                           #Der Highscore wird in score_save gespeichert
        self.Text.rendering(f'Score: {Settings.Score}' , 0 , 0, False)                                          #'Score:' wird gerendert
        self.Text.rendering(f'Highscore: {score_save}' , 0 , 50, False)                                         #'Highscore' wird gerendert

        if Settings.game_loos == True:                                                                          #Wenn game_loss True ist bzw. das Spiel verloren wurde...
            self.bubble_kollision.play()                                                                        #Wird der Sound für die Kollision der Bubbles abgespielt
            self.pause = True                                                                                   #self.pause wird auf True gesetzt, damit das Spiel im Hintergrund anhält
            self.screen.blit(self.brightness, (0, 0))                                                           #Das Bild wird dunkler gestellt
            self.Text.rendering(f'Your Score: {Settings.Score}' , 600, 200, False)                              #
            self.Text.rendering('You loosed' , 620, 300, False)                                                 #Diese drei Texte erscheinen bzw. werden gerendert
            self.Text.rendering('Press "R" to restart the game' , 400, 350, False)                              #
            pygame.mixer.music.pause()                                                                          #Die Hintergrundmusik wird pausiert
            Settings.game_loos = False                                                                          #game_loos wird wieder auf False gesetzt
            Settings.Score = 0                                                                                  #Der Score wird zurück gesetzt
#--------------------------------------------------------------------------------------------------------------------------------------------------------#

#----------------------------------------------------Speichert den Highscore-----------------------------------------------------------------------#
    def score_saver(self):
        aktueller_score = Settings.Score                                                                          #Der aktuelle Score wird in aktueller_score gespeichert
        alter_highscore = value_out_of_file('score', 'high_score.txt')                                            #Der aktuelle Highscore wird in alter_highscore durch das auslesen der .txt Datei gespeichert
        if alter_highscore == None:                                                                                   #Sollte nichts in alter_highscore gespeichert sein da in der .txt Datei kein Score gespeichert wurde, wird automatisch ein Score von 0 gesetzt 
            alter_highscore = 0                                                                                       #
        if aktueller_score > int(alter_highscore):                                                                      #Wenn der aktuelle Score größer ist als der vorherige Highscore, wird dieser überschrieben
            write_in_file('score', 'high_score.txt', str(aktueller_score), True)                                  #
#--------------------------------------------------------------------------------------------------------------------------------------------------#
    
        

        


if __name__ == '__main__':
                                    
    pygame.init()               # Bereitet die Module zur Verwendung vor  
    game = Game()
    game.run()
  
    pygame.quit()               # beendet pygame