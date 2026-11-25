


define config.name = _("Expediente213 (Caso Jeffery Dahmer)")



define gui.show_name = True

## Versión del juego.
define config.version = "1.0"

## Texto situado en la pantalla 'Acerca de' del juego. Sitúa el texto entre
## comillas triples y deja una línea en blanco entre párrafos.

define gui.about = _p("""
""")


define build.name = "Expediente213"


#Relleno del codigo

define config.has_sound = True
define config.has_music = True
define config.has_voice = True



define config.enter_transition = dissolve
define config.exit_transition = dissolve



define config.intra_transition = dissolve



define config.after_load_transition = None



define config.end_game_transition = None

define config.window = "auto"


define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)


## relleno codigo
default preferences.text_cps = 0
default preferences.afm_time = 15
 
#CODIGO PERSONALIZADO

define config.save_directory = "Expediente213-1788019700"

## El icono mostrado en la barra de tareas.

define config.window_icon = "gui/window_icon.png"

#RELLENO 
init python:

    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)

    build.documentation('*.html')
    build.documentation('*.txt')

define config.mouse = {
    'default': [ (im.Scale("gui/cursor.png", 24, 24), 0, 0) ]
}
