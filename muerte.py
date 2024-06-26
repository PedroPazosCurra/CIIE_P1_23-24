# -*- encoding: utf-8 -*-

from escena import *
from gestorRecursos import *


# -------------------------------------------------
# Clase abstracta ElementoGUI

class ElementoGUI:

    def __init__(self, pantalla, rectangulo):
        self.pantalla = pantalla
        self.rect = rectangulo

    def establecerPosicion(self, posicion):
        (posicionx, posiciony) = posicion
        self.rect.left = posicionx
        self.rect.bottom = posiciony

    def posicionEnElemento(self, posicion):
        (posicionx, posiciony) = posicion
        if (posicionx >= self.rect.left) and (posicionx <= self.rect.right) and (posiciony >= self.rect.top) and \
           (posiciony <= self.rect.bottom):
            return True
        else:
            return False

    def dibujar(self, pantalla):
        raise NotImplemented("Tiene que implementar el metodo dibujar.")

    def accion(self):
        raise NotImplemented("Tiene que implementar el metodo accion.")


# -------------------------------------------------
# Clase Boton y los distintos botones

class Boton(ElementoGUI):
    def __init__(self, pantalla, nombreImagen, posicion):
        # Se carga la imagen del boton
        self.imagen = GestorRecursos.CargarImagen(nombreImagen, -1)
        self.imagen = pygame.transform.scale(self.imagen, (400, 400))
        # Se llama al método de la clase padre con el rectángulo que ocupa el botón
        ElementoGUI.__init__(self, pantalla, self.imagen.get_rect())
        # Se coloca el rectangulo en su posicion
        self.establecerPosicion(posicion)

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)


class BotonJugar(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, 'boton_restart.png', (202, 733))

    def accion(self):
        self.pantalla.menu.ejecutarJuego()


class BotonSalir(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, 'boton_restart.png', (392, 733))

    def accion(self):
        self.pantalla.menu.salirPrograma()


# -------------------------------------------------
# Clase TextoGUI y los distintos textos

class TextoGUI(ElementoGUI):
    def __init__(self, pantalla, fuente, color, texto, posicion):
        # Se crea la imagen del texto
        self.imagen = fuente.render(texto, True, color)
        # Se llama al método de la clase padre con el rectángulo que ocupa el texto
        ElementoGUI.__init__(self, pantalla, self.imagen.get_rect())
        # Se coloca el rectangulo en su posicion
        self.establecerPosicion(posicion)

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)


class TextoJugar(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.SysFont('gabriola', 26)
        TextoGUI.__init__(self, pantalla, fuente, (0, 0, 0), 'Reset', (302, 535))

    def accion(self):
        self.pantalla.menu.ejecutarJuego()


class TextoSalir(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.SysFont('gabriola', 26)
        TextoGUI.__init__(self, pantalla, fuente, (0, 0, 0), 'Salir', (500, 535))

    def accion(self):
        self.pantalla.menu.salirPrograma()


# -------------------------------------------------
# Clase PantallaGUI y las distintas pantallas

class PantallaGUI:
    def __init__(self, menu, nombreImagen):
        self.elementoClic = None
        self.menu = menu
        # Se carga la imagen de fondo
        self.imagen = GestorRecursos.CargarImagen(nombreImagen)
        self.imagen = pygame.transform.scale(self.imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))
        # Se tiene una lista de elementos GUI
        self.elementosGUI = []

    def eventos(self, lista_eventos):
        for evento in lista_eventos:
            if evento.type == MOUSEBUTTONDOWN:
                self.elementoClic = None
                for elemento in self.elementosGUI:
                    if elemento.posicionEnElemento(evento.pos):
                        self.elementoClic = elemento
            if evento.type == MOUSEBUTTONUP:
                for elemento in self.elementosGUI:
                    if elemento.posicionEnElemento(evento.pos):
                        if elemento == self.elementoClic:
                            elemento.accion()

    def dibujar(self, pantalla):
        # Dibujamos primero la imagen de fondo
        pantalla.blit(self.imagen, self.imagen.get_rect())
        # Después los botones
        for elemento in self.elementosGUI:
            elemento.dibujar(pantalla)


class PantallaMuerteGUI(PantallaGUI):
    def __init__(self, menu):
        PantallaGUI.__init__(self, menu, 'pantalla_muerte.png')
        # Creamos los botones y los metemos en la lista
        botonJugar = BotonJugar(self)
        botonSalir = BotonSalir(self)
        self.elementosGUI.append(botonJugar)
        self.elementosGUI.append(botonSalir)
        # Creamos el texto y lo metemos en la lista

        textoJugar = TextoJugar(self)
        textoSalir = TextoSalir(self)
        self.elementosGUI.append(textoJugar)
        self.elementosGUI.append(textoSalir)


# -------------------------------------------------
# Clase Menu, la escena en sí

class Muerte(Escena):

    def __init__(self, director):
        # Llamamos al constructor de la clase padre
        Escena.__init__(self, director)
        self.pantallaActual = -1
        # Creamos la lista de pantallas
        self.listaPantallas = []
        # Creamos las pantallas que vamos a tener
        #   y las metemos en la lista
        self.listaPantallas.append(PantallaMuerteGUI(self))
        # En que pantalla estamos actualmente
        self.mostrarPantallaInicial()

        # Musica de muerte
        GestorRecursos.CargarMusica("musica_muerte.mp3")
        pygame.mixer.music.play(-1)

    def update(self, *args):
        return

    def eventos(self, lista_eventos):
        # Se mira si se quiere salir de esta escena
        for evento in lista_eventos:
            # Si se quiere salir, se le indica al director
            if evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    self.salirPrograma()
            elif evento.type == pygame.QUIT:
                self.director.salirPrograma()

        # Se pasa la lista de eventos a la pantalla actual
        self.listaPantallas[self.pantallaActual].eventos(lista_eventos)

    def dibujar(self, pantalla):
        self.listaPantallas[self.pantallaActual].dibujar(pantalla)

    # --------------------------------------
    # Metodos propios del menu

    def salirPrograma(self):
        self.director.salirPrograma()

    def ejecutarJuego(self):

        # TODO Esta es una aproximación incorrecta para hacer el workaround. La música hay que manejarla en otro lado.
        GestorRecursos.CargarMusica("musica_menu.mp3")
        pygame.mixer.music.play(-1)
        self.director.salirEscena()

    def mostrarPantallaInicial(self):
        self.pantallaActual = 0

    # def mostrarPantallaConfiguracion(self):
    #    self.pantallaActual = ...
