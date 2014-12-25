#!/usr/bin/python

import gobject
import dbus
import dbus.service
import dbus.mainloop.glib
import signal
import os
import pygame
import time
import logging
import logging.handlers

class Tombolone(dbus.service.Object) :
    screen = None
    size = None
    larghezza = 0
    altezza = 0

    coloreLineaBordo = (0, 0, 0)
    coloreLineaInterna = (64, 64, 64)
    spessore_linea_esterna = 2
    coloreTitolo = (204, 0, 0)
    testoTitolo = "Tombolone - Oratorio Parrocchiale S. Domenico Savio"
    dimensioneTestoTitolo = 24
    coloreSfondoNumeriEstratti = (153, 255, 153)
    dimensioneNumeri = 40
    coloreNumeriEstratti = (0, 0, 0)
    coloreNumeri = (0, 0, 255)
    coloreSfondo = (255, 255, 255)
    coloreVittoria = (255, 255, 0)
    dimensioneVittoria = 140
    estratti = []
    img_path = '/tombolone/backgrounds/sfondo.png'
    img = None

    def __init__(self):
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            my_logger.debug("I'm running under X display = %s" % disp_no )

        drivers = ['fbcon', 'directfb', 'svgalib']
        found = False
        for driver in drivers:
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                my_logger.warning('Driver: %s failed...' % driver )
                continue
            found = True
            my_logger.info('Driver: %s OK.' % driver )
            break
    
        if not found:
            my_logger.error('No suitable video driver found!')
            raise Exception('No suitable video driver found!')
        
        self.size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.larghezza = self.size[0]
        self.altezza = self.size[1]
        my_logger.debug("Framebuffer size: %d x %d" % (self.size[0], self.size[1]))
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)        

        pygame.font.init()

        pygame.mixer.init()

        self.estrattosound = pygame.mixer.Sound('/tombolone/sounds/1.ogg')
        #self.ternosound = pygame.mixer.Sound('/tombolone/sounds/2.ogg')
        self.premisound = pygame.mixer.Sound('/tombolone/sounds/3.ogg')
        #self.cinquinasound = pygame.mixer.Sound('/tombolone/sounds/4.ogg')
        self.tombolasound = pygame.mixer.Sound('/tombolone/sounds/5.ogg')

        pygame.mouse.set_visible(False)

        self.img = pygame.image.load(self.img_path)

        self.fontTitolo = pygame.font.Font('/tombolone/fonts/MeriendaOne.ttf', self.dimensioneTestoTitolo)
        self.fontVittoria = pygame.font.Font('/tombolone/fonts/courgette.ttf', self.dimensioneVittoria)

        self.aggiornaTabellone()

        bus_name = dbus.service.BusName('it.parrocchiasangiacomobianchi.tombolone', bus=dbus.SystemBus())
        dbus.service.Object.__init__(self, bus_name, '/')

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

    def disegnaTabellone(self):
        self.screen.fill(self.coloreSfondo)

        self.screen.blit(self.img,(0,0))

        pygame.draw.rect(self.screen, self.coloreLineaBordo, (0,0,self.larghezza-self.spessore_linea_esterna/2,self.altezza-self.spessore_linea_esterna/2), self.spessore_linea_esterna)

        # title rect
        pygame.draw.line(self.screen, self.coloreLineaInterna,(0,self.altezza/10),(self.larghezza,self.altezza/10))

        # Display title
	text = self.fontTitolo.render(self.testoTitolo, 1, self.coloreTitolo)
	textpos = text.get_rect()
	textpos.centerx = self.larghezza/2
        textpos.centery = self.altezza/10/2
	self.screen.blit(text, textpos)

        # Horizontal lines
        for i in range(1, 9):
            y = self.altezza/10 + i*self.altezza/10
            pygame.draw.line(self.screen, self.coloreLineaInterna, (0, y), (self.larghezza, y))

        # Vertical lines
        for i in range(1, 10):
            x = i*self.larghezza/10
            pygame.draw.line(self.screen, self.coloreLineaInterna, (x, self.altezza/10), (x, self.altezza))

    def aggiornaEstratti(self):

        for num in self.estratti:
            x = self.spessore_linea_esterna + self.larghezza/10*((num-1)%10)
            y = self.altezza/10 + self.altezza/10*((num-1)/10) +1
            pygame.draw.rect(self.screen, self.coloreSfondoNumeriEstratti, pygame.Rect((x+(((num-1)%10)/2),y+1), (self.larghezza/10-2,self.altezza/10-2)))

        for i in range(0,90):
            x = self.larghezza/10/2 + self.larghezza/10*(i%10)
            y = self.altezza/10 + self.altezza/10/2 + self.altezza/10*(i/10)
            font = pygame.font.Font(None, self.dimensioneNumeri)
            text = font.render(str(i+1), 1, self.coloreNumeriEstratti if i+1 in self.estratti else self.coloreNumeri)
            textpos = text.get_rect()
	    textpos.centerx = x+(((i-1)%10)/2)
            textpos.centery = y
	    self.screen.blit(text, textpos)

    @dbus.service.method("it.parrocchiasangiacomobianchi.Interface", in_signature='s', out_signature='')
    def aggiungiOEliminaEstratto(self, num):
        num = int(num)
        if num not in self.estratti:
            self.estratti.append(num)
            my_logger.debug("disegno il numero 1")
            self.disegnaEstratto(num)
            self.estrattosound.play()
            my_logger.debug("disegno il numero 5")
            pygame.time.wait(int(self.estrattosound.get_length()*1000))
            my_logger.debug("disegno il numero 6")
        else:
            self.estratti.remove(num)
        self.aggiornaTabellone()

    def disegnaEstratto(self, num):
        my_logger.debug("disegno il numero 2")
        #wood = (222,184,135)
        wood = (205, 133, 63)
        red = (255, 0, 0)
        pygame.draw.circle(self.screen, wood, (self.larghezza/2,self.altezza/2), int(self.altezza/4), 0)
        pygame.draw.circle(self.screen, self.coloreTitolo, (self.larghezza/2,self.altezza/2), int(self.altezza/4-5), 0)
        pygame.draw.circle(self.screen, wood, (self.larghezza/2,self.altezza/2), int(self.altezza/4-20), 0)
        my_logger.debug("disegno il numero 3")
        numfont = pygame.font.Font(None, 220)
        text = numfont.render(str(num), 1, self.coloreTitolo)
        textpos = text.get_rect()
        textpos.centerx = self.larghezza/2
        textpos.centery = self.altezza/2
        self.screen.blit(text,textpos)
        my_logger.debug("disegno il numero 4")
        pygame.display.flip()

    @dbus.service.method("it.parrocchiasangiacomobianchi.Interface", in_signature='', out_signature='')
    def ricominciaGioco(self):
        self.estratti = []
        self.aggiornaTabellone()

    def aggiornaTabellone(self):
        self.disegnaTabellone()
        self.aggiornaEstratti()
        pygame.display.flip()

    @dbus.service.method("it.parrocchiasangiacomobianchi.Interface", in_signature='s', out_signature='')
    def vittoria(self, testo):
        text = self.fontVittoria.render(testo, 1, self.coloreVittoria)
        textpos = text.get_rect()
        textpos.centerx = self.larghezza/2
        textpos.centery = self.altezza/2
        self.screen.blit(text,textpos)
        pygame.display.flip()
        if testo == "Ambo!":
            self.premisound.play()
            pygame.time.wait(int(self.premisound.get_length()*1000))
        elif testo == "Terno!":
            self.premisound.play()
            pygame.time.wait(int(self.premisound.get_length()*1000))
        elif testo == "Quaterna!":
            self.premisound.play()
            pygame.time.wait(int(self.premisound.get_length()*1000))
        elif testo == "Cinquina!":
            self.premisound.play()
            pygame.time.wait(int(self.premisound.get_length()*1000))
        elif testo == "Tombola!":
            self.tombolasound.play()
            pygame.time.wait(int(self.tombolasound.get_length()*1000))
        else:
            pygame.time.wait(5000)
        self.aggiornaTabellone()

    @dbus.service.method("it.parrocchiasangiacomobianchi.Interface", in_signature='', out_signature='ai')
    def get_estratti(self):
        return self.estratti

def killSigHandler(signum, frame):
    my_logger.info('Exiting...')
    my_logger.shutdown()
    mainloop.quit()

signal.signal(signal.SIGINT, killSigHandler)
signal.signal(signal.SIGHUP, killSigHandler)
signal.signal(signal.SIGTERM, killSigHandler)

my_logger = logging.getLogger('Tombolone')
my_logger.setLevel(logging.DEBUG)
my_handler = logging.handlers.RotatingFileHandler('/tmp/tombolone.log', maxBytes=102400, backupCount=1)
my_handler.setLevel(logging.DEBUG)
my_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
my_handler.setFormatter(my_formatter)
my_logger.addHandler(my_handler)

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

my_logger.info('Starting...')

t = Tombolone()

my_logger.info('Started...')

mainloop = gobject.MainLoop()
mainloop.run()
