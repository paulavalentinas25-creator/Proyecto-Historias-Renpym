

init offset = -1


#Relleno

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)



#PANTALLAS JUEGO 
## https://www.renpy.org/doc/html/screen_special.html#say

screen say(who, what):

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"


    ## Si hay una imagen lateral, la muestra encima del texto. No la muestra en
    ## la variante de teléfono - no hay lugar.
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0


## Permite que el 'namebox' pueda ser estilizado en el objeto 'Character'.
init python:
    config.character_id_prefixes.append('namebox')

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos

    adjust_spacing False

## Pantalla de introducción de texto ###########################################
##
## Pantalla usada para visualizar 'renpy.input'. El parámetro 'prompt' se usa
## para pasar el texto presentado.
##
## Esta pantalla debe crear un displayable 'input' con id "input" para aceptar
## diversos parámetros de entrada.
##
## https://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xanchor gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


## Pantalla de menú ############################################################
##
## Esta pantallla presenta las opciones internas al juego de la sentencia
## 'menu'. El parámetro único, 'items', es una lista de objetos, cada uno los
## campos 'caption' y 'action'.
##
## https://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 405
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.text_properties("choice_button")


## Pantalla de menú rápido #####################################################
##
## El menú rápido se presenta en el juego para ofrecer fácil acceso a los menus
## externos al juego.

screen quick_menu():

    ## Asegura que esto aparezca en la parte superior de otras pantallas.
    zorder 100

    if quick_menu:

        hbox:
            style_prefix "quick"
            style "quick_menu"

            textbutton _("Atrás") action Rollback()
            textbutton _("Historial") action ShowMenu('history')
            textbutton _("Saltar") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Guardar") action ShowMenu('save')
            textbutton _("Cargar R.") action QuickLoad()
            textbutton _("Prefs.") action ShowMenu('preferences')


## Este código asegura que la pantalla 'quick_menu' se muestra en el juego,
## mientras el jugador no haya escondido explícitamente la interfaz.
init python:
    config.overlay_screens.append("quick_menu")

default quick_menu = True

style quick_menu is hbox
style quick_button is default
style quick_button_text is button_text

style quick_menu:
    xalign 0.5
    yalign 1.0

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.text_properties("quick_button")


################################################################################
## Principal y Pantalla de menu del juego.
################################################################################

## Pantalla de navegación ######################################################
##
## Esta pantalla está incluída en el menú principal y los menús del juego y
## ofrece navegación a los otros menús y al inicio del juego.
screen navigation():

    vbox:
        style_prefix "navigation"
        xalign 0.99
        yalign 0.45
        spacing 8

        if main_menu:
            textbutton _("> ABRIR EXPEDIENTE") action Start("caso_dahmer_inicio")
            textbutton _("> REVISAR ARCHIVOS") action Show("revisar_archivos")
            textbutton _("> AJUSTES DE EVIDENCIA") action Show("ajustes_evidencia")
            textbutton _("> CREDITOS") action Show("creditos_expediente")
            textbutton _("> CERRAR CASO") action MainMenu()
        else:
            textbutton _("Guardar") action ShowMenu("save")
            textbutton _("Cargar") action ShowMenu("load")
            textbutton _("Opciones") action ShowMenu("preferences")
            textbutton _("Menu principal") action MainMenu()
            textbutton _("Salir") action Quit()

        if _in_replay:

            textbutton _("Finaliza repeticion") action EndReplay(confirm=True)

        elif not main_menu:

            textbutton _("Menu principal") action MainMenu()

        textbutton _("Acerca de") action Show("acerca_de_expediente")

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):

            ## La ayuda no es necesaria ni relevante en dispositivos móviles.
            textbutton _("Ayuda") action Show("ayuda_expediente")

        if renpy.variant("pc"):

            ## El botón de salida está prohibido en iOS y no es necesario en
            ## Android y Web.
            textbutton _("Salir") action Quit(confirm=not main_menu)


style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    properties gui.text_properties("navigation_button")


## ---------------------------------------------------------
## PANTALLAS PERSONALIZADAS DEL MENÚ DEL EXPEDIENTE
## ---------------------------------------------------------

screen revisar_archivos():
    modal True

    frame:
        background "#000000cc"
        padding (40, 32)
        xalign 0.5
        yalign 0.5

        vbox:
            spacing 18
            xalign 0.5

            textbutton _("X") action Hide("revisar_archivos") xalign 0.5

            label _("REVISAR ARCHIVOS") xalign 0.5

            textbutton _("CAP 1 — La llamada al 911"):
                action [Hide("revisar_archivos"), Start("caso_dahmer_inicio")]
                xalign 0.5

            textbutton _("CAP 2 — La captura (Apto. 213)"):
                action [Hide("revisar_archivos"), Start("cap_2_captura")]
                xalign 0.5

            textbutton _("CAP 3 — Entrevista en prision"):
                action [Hide("revisar_archivos"), Start("escena_entrevista")]
                xalign 0.5

            null height 8

            textbutton _("Volver al expediente"):
                action Hide("revisar_archivos")
                xalign 0.5


screen ajustes_evidencia():
    modal True

    frame:
        background "#000000cc"
        padding (40, 32)
        xalign 0.5
        yalign 0.5

        vbox:
            spacing 16
            xalign 0.5

            textbutton _("X") action Hide("ajustes_evidencia") xalign 0.5

            label _("AJUSTES DE EVIDENCIA") xalign 0.5

            if config.has_music:
                label _("Volumen de musica") xalign 0.5
                bar value Preference("music volume") xsize 450

            if config.has_sound:
                label _("Volumen de sonido") xalign 0.5
                bar value Preference("sound volume") xsize 450

            if config.has_voice:
                label _("Volumen de voz") xalign 0.5
                bar value Preference("voice volume") xsize 450

            textbutton _("Silenciar / Activar todo"):
                action Preference("all mute", "toggle")
                xalign 0.5

            null height 8

            textbutton _("Volver al expediente"):
                action Hide("ajustes_evidencia")
                xalign 0.5


screen creditos_expediente():
    modal True

    frame:
        background "#db1c1ccc"
        padding (40, 32)
        xalign 0.5
        yalign 0.5

        vbox:
            spacing 14
            xalign 0.5

            textbutton _("X") action Hide("creditos_expediente") xalign 0.5

            label _("CREDITOS") xalign 0.5
            text _("Paula Solano") size 28 xalign 0.5
            text _("Jeronimo Rojas") size 28 xalign 0.5
            text _("David Triana") size 28 xalign 0.5

            null height 8

            textbutton _("Volver al expediente"):
                action Hide("creditos_expediente")
                xalign 0.5

screen acerca_de_expediente():
    modal True

    frame:
        background "#000000cc"
        padding (40, 32)
        xalign 0.5
        yalign 0.5
        xmaximum 680

        vbox:
            spacing 16
            xalign 0.5

            textbutton _("X") action Hide("acerca_de_expediente") xalign 0.5

            label _("ACERCA DE") xalign 0.5

            text _("Expediente 213 (Caso Jeffery Dahmer)") size 26 xalign 0.5
            text _("Novela visual interactiva desarrollada en Ren'Py con logica personalizada en Python, no tiene acentos por cuestiones de procesamiento") size 22 xalign 0.5 text_align 0.5
            text _("Autores: Paula Solano, Jeronimo Rojas y David Triana.") size 22 xalign 0.5 text_align 0.5

            null height 8

            textbutton _("Volver al expediente"):
                action Hide("acerca_de_expediente")
                xalign 0.5


screen ayuda_expediente():
    modal True

    frame:
        background "#000000cc"
        padding (40, 32)
        xalign 0.5
        yalign 0.5
        xmaximum 700

        vbox:
            spacing 16
            xalign 0.5

            textbutton _("X") action Hide("ayuda_expediente") xalign 0.5

            label _("AYUDA") xalign 0.5

            text _("• Usa el raton o clic izquierdo para avanzar en los dialogos y elegir opciones.") size 22 xalign 0.5 text_align 0.5
            text _("• En REVISAR ARCHIVOS puedes saltar directamente a los capitulos 1, 2 o 3.") size 22 xalign 0.5 text_align 0.5
            text _("• En AJUSTES DE EVIDENCIA puedes regular el volumen de musica, sonido y voz.") size 22 xalign 0.5 text_align 0.5
            text _("• Pulsa ESC o clic derecho durante la partida para abrir el menu rpido.") size 22 xalign 0.5 text_align 0.5

            null height 8

            textbutton _("Volver al expediente"):
                action Hide("ayuda_expediente")
                xalign 0.5

screen expediente_proximamente():
    modal True

    add "#000000"

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 28

        text _("PROXIMAMENTE"):
            color "#ff2b2b"
            size 64
            bold True
            xalign 0.5

        textbutton _("Volver"):
            action Hide("expediente_proximamente")
            xalign 0.5
## Pantalla del menú principal #################################################
##
## Usado para mostrar el menú principal cuando Ren'Py arranca.
##
## https://www.renpy.org/doc/html/screen_special.html#main-menu

# Animación ATL para el logo (parpadeo de estática y vibración)
transform tv_interferencia:    # Quita el fondo negro y le da brillo CRT de forma nativa
    alpha 0.85
    additive 1.0
    pause 0.08
    alpha 1.0
    xoffset 1
    pause 0.04
    xoffset -1
    alpha 0.75
    pause 0.1
    xoffset 0
    alpha 0.95
    pause 0.05
    repeat
    

screen expediente_dahmer():
    tag menu

    # Fondo de la TV
    add "gui/main_menu.png"

    # Logo incrustado dentro de la TV (Aquí va el cambio)
    add "gui/logo.png":
        at tv_interferencia
        anchor (0.5,0.5)
        xpos 0.40
        ypos 0.40
        zoom 0.80

    use navigation

    # Botón discreto abajo para volver al menú de selección general
    textbutton "< VOLVER A EXPEDIENTES" action ShowMenu("main_menu"):
        xalign 0.05
        yalign 0.95
        text_size 16

screen main_menu():
    tag menu

    # Fondo de escritorio Windows 
    add "gui/windows.png" fit "cover" 
    
    draggroup:

        # 🗑️ PAPELERA DE RECICLAJE (Fija abajo a la izquierda)
        drag:
            drag_name "papelera"
            xpos 40 ypos 450
            draggable False
            droppable True

            vbox: 
                spacing 5
                add "gui/papelera.png" xalign 0.5 zoom 0.25
                text "Papelera de\nReciclaje" size 12 color "#ffffff" text_align 0.5 xalign 0.5

            
        # -----------------------------------------------------------------
        # EXPEDIENTES FIJOS (Columna izquierda: X=40)
        # -----------------------------------------------------------------
        drag:
            drag_name "exp_dahmer"
            xpos 40 ypos 30
            draggable False
            droppable False
            button:
                action ShowMenu("expediente_dahmer")
                vbox: 
                    spacing 5
                    add "gui/folder.png" xalign 0.5 zoom 0.25
                    text "[[EXPEDIENTE 213]]\nDahmer.exe" size 12 color "#ffffff" text_align 0.5 xalign 0.5

        drag:
            drag_name "exp_clasificado"
            xpos 40 ypos 160
            draggable False
            droppable False
            button: 
                action Show("expediente_proximamente")
                vbox:
                    spacing 5
                    add "gui/folder.png" xalign 0.5 zoom 0.25
                    text "[[EXPEDIENTE 002]]\nClasificado.exe" size 12 color "#ffffff" text_align 0.5 xalign 0.5

        drag:
            drag_name "exp_caso3"
            xpos 40 ypos 290
            draggable False
            droppable False
            button:
                action Show("expediente_proximamente")
                vbox:
                    spacing 5
                    add "gui/folder.png" xalign 0.5 zoom 0.25
                    text "[[EXPEDIENTE 003]]\nCaso_3.exe" size 12 color "#ffffff" text_align 0.5 xalign 0.5

        # -----------------------------------------------------------------
        # ARCHIVOS DINÁMICOS SUBIDOS/LOCALES (Columna derecha: X=200+)
        # -----------------------------------------------------------------
        $ todos_los_archivos = obtener_historias()
        $ activos = [a for a in todos_los_archivos if a not in papelera]

        for idx, archivo in enumerate(activos):
            $ col = idx // 4
            $ fila = idx % 4
            $ pos_x = 220 + (col * 150)
            $ pos_y = 30 + (fila * 125)
            $ _item_web = buscar_item_cargado(archivo)

            drag:
                drag_name archivo
                xpos pos_x ypos pos_y
                draggable True
                droppable False
                dragged elemento_soltado_en_papelera
                
                # Clic derecho / secundario para abrir
                alternate Function(abrir_archivo, archivo)

                vbox:
                    spacing 5
                    xmaximum 110

                    if _item_web is not None and isinstance(_item_web.get("contenido"), str) and _item_web["contenido"].startswith("data:image"):
                        add Transform(_item_web["contenido"], size=(50, 50), xalign=0.5)
                    elif archivo.lower().endswith(('.png', '.jpg', '.jpeg')):
                        add Transform("historias/" + archivo, size=(50, 50), xalign=0.5)
                    elif archivo.lower().endswith(('.doc', '.docx')):
                        add "gui/folder.png" xalign 0.5 zoom 0.25
                    elif archivo.lower().endswith('.pdf'):
                        add "gui/folder.png" xalign 0.5 zoom 0.25
                    elif archivo.lower().endswith(('.txt', '.rpy')):
                        add "gui/folder.png" xalign 0.5 zoom 0.25
                    else:
                        add "gui/folder.png" xalign 0.5 zoom 0.25

                    text archivo size 10 color "#ffffff" text_align 0.5 xalign 0.5

    # BARRA DE TAREAS INFERIOR
    frame:
        xalign 0.0
        yalign 1.0
        xfill True
        ysize 38
        background Solid("#c0c0c0")

        hbox:
            yalign 0.5
            xpos 5
            spacing 10

            textbutton " [[START]] Apagar Sistema " action Quit():
                text_color "#000000"
                text_size 13
                background Solid("#dfdfdf")

            textbutton " [[UPLOAD]] Subir Historia " action Function(subir_archivo_multimedia):
                text_color "#000000"
                text_size 13
                background Solid("#dfdfdf")

            textbutton " Vaciar Papelera " action Function(vaciar_papelera):
                text_color "#000000"
                text_size 13
                background Solid("#dfdfdf")

    # RELOJ DE LA BARRA DE TAREAS
    frame:
        xalign 0.99
        yalign 0.99
        padding (8, 4)
        background Solid("#a0a0a0")
        text "11:59 PM" size 12 color "#000000"

# VISOR DE IMÁGENES DENTRO DEL JUEGO
screen visor_imagenes():
    modal True
    zorder 100

    # Ventana estilo retro
    frame:
        xalign 0.5 yalign 0.5
        background Solid("#c0c0c0")
        padding (10, 10)

        vbox:
            spacing 10

            # Barra de título
            frame:
                xfill True
                ysize 25
                background Solid("#000080")
                hbox:
                    xpos 5 yalign 0.5
                    text "Visor de Imágenes" size 12 color "#ffffff" bold True
                
                # Botón X para cerrar
                textbutton " X " action Hide("visor_imagenes"):
                    xalign 1.0 yalign 0.5
                    background Solid("#c0c0c0")
                    text_color "#000000"
                    text_size 10

            # Contenido de la imagen ajustado
            add Transform(visor_archivo_actual, maxsize=(800, 600))

# VISOR DE TEXTO / NOTAS DENTRO DEL JUEGO
screen visor_texto(titulo, contenido):
    modal True
    zorder 100

    frame:
        xalign 0.5 yalign 0.5
        xsize 600 ysize 400
        background Solid("#c0c0c0")
        padding (10, 10)

        vbox:
            spacing 10

            # Barra de título estilo Bloc de notas
            frame:
                xfill True
                ysize 25
                background Solid("#000080")
                hbox:
                    xpos 5 yalign 0.5
                    text titulo size 12 color "#ffffff" bold True
                
                textbutton " X " action Hide("visor_texto"):
                    xalign 1.0 yalign 0.5
                    background Solid("#c0c0c0")
                    text_color "#000000"
                    text_size 10

            # Caja de texto
            frame:
                xfill True yfill True
                background Solid("#ffffff")
                padding (10, 10)
                viewport id "vp_texto":
                    draggable True
                    mousewheel True
                    scrollbars "vertical"
                    text contenido color "#000000" size 14


style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text

style main_menu_frame:
    xsize 420
    yfill True

    background "gui/overlay/main_menu"

style main_menu_vbox:
    xalign 1.0
    xoffset -30
    xmaximum 1200
    yalign 1.0
    yoffset -30

style main_menu_text:
    properties gui.text_properties("main_menu", accent=True)

style main_menu_title:
    properties gui.text_properties("title")

style main_menu_version:
    properties gui.text_properties("version")



## Pantalla del menú del juego #################################################
##
## Esto distribuye la estructura de base del menú del juego. Es llamado con el
## título de la pantalla y presenta el fondo, el título y la navegación.
##
## El parámetro 'scroll' puede ser 'None', "viewport" o "vpgrid". Se usa esta
## pantalla con uno o más elementos, que son transcluídos (situados) en su
## interior.

screen game_menu(title, scroll=None, yinitial=0.0, spacing=0):

    style_prefix "game_menu"

    if main_menu:
        add "#000000cc"
    else:
        add "#000000cc"

    frame:
        style "game_menu_outer_frame"

        hbox:

            ## Reservar espacio para la sección de navegación.
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        vbox:
                            spacing spacing

                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial yinitial

                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        spacing spacing

                        transclude

                else:

                    transclude

    use navigation

    textbutton _("Volver"):
        style "return_button"

        action Return()

    label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding 45
    top_padding 180

    background "gui/overlay/game_menu.png"

style game_menu_navigation_frame:
    xsize 420
    yfill True

style game_menu_content_frame:
    left_margin 60
    right_margin 30
    top_margin 15

style game_menu_viewport:
    xsize 1380

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 15

style game_menu_label:
    xpos 75
    ysize 180

style game_menu_label_text:
    size 75
    color gui.accent_color
    yalign 0.5

style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -45


## Pantalla 'acerca de' ########################################################
##
## Esta pantalla da información sobre los créditos y el copyright del juego y de
## Ren'Py.
##
## No hay nada especial en esta pantalla y por tanto sirve también como ejemplo
## de cómo hacer una pantalla personalizada.

screen about():

    tag menu

    ## Esta sentencia 'use' incluye la pantalla 'game_menu' dentro de esta. El
    ## elemento 'vbox' se incluye entonces dentro del 'viewport' al interno de
    ## la pantalla 'game_menu'.
    use game_menu(_("Acerca de"), scroll="viewport"):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("Versión [config.version!t]\n")

            ## 'gui.about' se ajusta habitualmente en 'options.rpy'.
            if gui.about:
                text "[gui.about!t]\n"

            text _("Hecho con {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size


## Pantallas de carga y grabación ##############################################
##
## Estas pantallas permiten al jugador grabar el juego y cargarlo de nuevo. Como
## comparten casi todos los elementos, ambas están implementadas en una tercera
## pantalla: 'file_slots'.
##
## https://www.renpy.org/doc/html/screen_special.html#save https://
## www.renpy.org/doc/html/screen_special.html#load

screen save():

    tag menu

    use file_slots(_("Guardar"))


screen load():

    tag menu

    use file_slots(_("Cargar"))


screen file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("Página {}"), auto=_("Grabación automática"), quick=_("Grabación rápida"))

    use game_menu(title):

        fixed:

            ## Esto asegura que 'input' recibe el evento 'enter' antes que otros
            ## botones.
            order_reverse True

            ## El nombre de la pagina, se puede editar haciendo clic en el
            ## botón.
            button:
                style "page_label"

                key_events True
                xalign 0.5
                action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value

            ## La cuadrícula de huecos de guardado.
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.5

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action FileAction(slot)

                        has vbox

                        add FileScreenshot(slot) xalign 0.5

                        text FileTime(slot, format=_("{#file_time}%A, %d de %B %Y, %H:%M"), empty=_("vacío")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)

            ## Botones de acceso a otras páginas
            vbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0

                hbox:
                    xalign 0.5

                    spacing gui.page_spacing

                    textbutton _("<") action FilePagePrevious()
                    key "save_page_prev" action FilePagePrevious()

                    if config.has_autosave:
                        textbutton _("{#auto_page}A") action FilePage("auto")

                    if config.has_quicksave:
                        textbutton _("{#quick_page}R") action FilePage("quick")

                    ## range(1, 10) da los números del 1 al 9.
                    for page in range(1, 10):
                        textbutton "[page]" action FilePage(page)

                    textbutton _(">") action FilePageNext()
                    key "save_page_next" action FilePageNext()

                if config.has_sync:
                    if CurrentScreenName() == "save":
                        textbutton _("Subir Sync"):
                            action UploadSync()
                            xalign 0.5
                    else:
                        textbutton _("Descargar Sync"):
                            action DownloadSync()
                            xalign 0.5


style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    xpadding 75
    ypadding 5
    xalign 0.5

style page_label_text:
    textalign 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.text_properties("page_button")

style slot_button:
    properties gui.button_properties("slot_button")

style slot_button_text:
    properties gui.text_properties("slot_button")


## Pantalla de preferencias ####################################################
##
## La pantalla de preferencias permite al jugador configurar el juego a su
## gusto.
##
## https://www.renpy.org/doc/html/screen_special.html#preferences

screen preferences():

    tag menu

    use game_menu(_("Opciones"), scroll="viewport"):

        vbox:

            hbox:
                box_wrap True

                if renpy.variant("pc") or renpy.variant("web"):

                    vbox:
                        style_prefix "radio"
                        label _("Pantalla")
                        textbutton _("Ventana") action Preference("display", "window")
                        textbutton _("Pantalla completa") action Preference("display", "fullscreen")

                vbox:
                    style_prefix "check"
                    label _("Saltar")
                    textbutton _("Texto no visto") action Preference("skip", "toggle")
                    textbutton _("Tras elecciones") action Preference("after choices", "toggle")
                    textbutton _("Transiciones") action InvertSelected(Preference("transitions", "toggle"))

                ## Aquí se pueden añadir 'vboxes' adicionales del tipo
                ## "radio_pref" o "check_pref" para nuevas preferencias.

            null height (4 * gui.pref_spacing)

            hbox:
                style_prefix "slider"
                box_wrap True

                vbox:

                    label _("Veloc. texto")

                    bar value Preference("text speed")

                    label _("Veloc. autoavance")

                    bar value Preference("auto-forward time")

                vbox:

                    if config.has_music:
                        label _("Volumen música")

                        hbox:
                            bar value Preference("music volume")

                    if config.has_sound:

                        label _("Volumen sonido")

                        hbox:
                            bar value Preference("sound volume")

                            if config.sample_sound:
                                textbutton _("Prueba") action Play("sound", config.sample_sound)


                    if config.has_voice:
                        label _("Volumen voz")

                        hbox:
                            bar value Preference("voice volume")

                            if config.sample_voice:
                                textbutton _("Prueba") action Play("voice", config.sample_voice)

                    if config.has_music or config.has_sound or config.has_voice:
                        null height gui.pref_spacing

                        textbutton _("Silenciar todo"):
                            action Preference("all mute", "toggle")
                            style "mute_all_button"


style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 3

style pref_label_text:
    yalign 1.0

style pref_vbox:
    xsize 338

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/radio_[prefix_]foreground.png"

style radio_button_text:
    properties gui.text_properties("radio_button")

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.text_properties("check_button")

style slider_slider:
    xsize 525

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 15

style slider_button_text:
    properties gui.text_properties("slider_button")

style slider_vbox:
    xsize 675


## Pantalla de historial #######################################################
##
## Esta pantalla presenta el historial de diálogo al jugador, almacenado en
## '_history_list'.
##
## https://www.renpy.org/doc/html/history.html

screen history():

    tag menu

    ## Evita la predicción de esta pantalla, que podría ser demasiado grande.
    predict False

    use game_menu(_("Historial"), scroll=("vpgrid" if gui.history_height else "viewport"), yinitial=1.0, spacing=gui.history_spacing):

        style_prefix "history"

        for h in _history_list:

            window:

                ## Esto distribuye los elementos apropiadamente si
                ## 'history_height' es 'None'.
                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"
                        substitute False

                        ## Toma el color del texto 'who' de 'Character', si ha
                        ## sido establecido.
                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                text what:
                    substitute False

        if not _history_list:
            label _("El historial está vacío.")


## Esto determina qué etiquetas se permiten en la pantalla de historial.

define gui.history_allow_tags = { "alt", "noalt", "rt", "rb", "art" }


style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    textalign gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    textalign gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5


## Pantalla de ayuda ###########################################################
##
## Una pantalla que da información sobre el uso del teclado y el ratón. Usa
## otras pantallas con el contenido de la ayuda ('keyboard_help', 'mouse_help',
## y 'gamepad_help').

screen help():

    tag menu

    default device = "keyboard"

    use game_menu(_("Ayuda"), scroll="viewport"):

        style_prefix "help"

        vbox:
            spacing 23

            hbox:

                textbutton _("Teclado") action SetScreenVariable("device", "keyboard")
                textbutton _("Ratón") action SetScreenVariable("device", "mouse")

                if GamepadExists():
                    textbutton _("Mando") action SetScreenVariable("device", "gamepad")

            if device == "keyboard":
                use keyboard_help
            elif device == "mouse":
                use mouse_help
            elif device == "gamepad":
                use gamepad_help


screen keyboard_help():

    hbox:
        label _("Intro")
        text _("Avanza el diálogo y activa la interfaz.")

    hbox:
        label _("Espacio")
        text _("Avanza el diálogo sin seleccionar opciones.")

    hbox:
        label _("Teclas de flecha")
        text _("Navega la interfaz.")

    hbox:
        label _("Escape")
        text _("Accede al menú del juego.")

    hbox:
        label _("Ctrl")
        text _("Salta el diálogo mientras se presiona.")

    hbox:
        label _("Tabulador")
        text _("Activa/desactiva el salto de diálogo.")

    hbox:
        label _("Av. pág.")
        text _("Retrocede al diálogo anterior.")

    hbox:
        label _("Re. pág.")
        text _("Avanza hacia el diálogo siguiente.")

    hbox:
        label "H"
        text _("Oculta la interfaz.")

    hbox:
        label "S"
        text _("Captura la pantalla.")

    hbox:
        label "V"
        text _("Activa/desactiva la asistencia por {a=https://www.renpy.org/l/voicing}voz-automática{/a}.")

    hbox:
        label "Shift+A"
        text _("Abre el menú de accesibilidad.")


screen mouse_help():

    hbox:
        label _("Clic izquierdo")
        text _("Avanza el diálogo y activa la interfaz.")

    hbox:
        label _("Clic medio")
        text _("Oculta la interfaz.")

    hbox:
        label _("Clic derecho")
        text _("Accede al menú del juego.")

    hbox:
        label _("Rueda del ratón arriba")
        text _("Retrocede al diálogo anterior.")

    hbox:
        label _("Rueda del ratón abajo")
        text _("Avanza hacia el diálogo siguiente.")


screen gamepad_help():

    hbox:
        label _("Gatillo derecho\nA/Botón inferior")
        text _("Avanza el diálogo y activa la interfaz.")

    hbox:
        label _("Gatillo izquierdo\nBotón sup. frontal izq.")
        text _("Retrocede al diálogo anterior.")

    hbox:
        label _("Botón sup. frontal der.")
        text _("Avanza hacia el diálogo siguiente.")

    hbox:
        label _("D-Pad, Sticks")
        text _("Navega la interfaz.")

    hbox:
        label _("Inicio, Guía, B/Botón Derecho")
        text _("Accede al menú del juego.")

    hbox:
        label _("Y/Botón superior")
        text _("Oculta la interfaz.")

    textbutton _("Calibrar") action GamepadCalibrate()


style help_button is gui_button
style help_button_text is gui_button_text
style help_label is gui_label
style help_label_text is gui_label_text
style help_text is gui_text

style help_button:
    properties gui.button_properties("help_button")
    xmargin 12

style help_button_text:
    properties gui.text_properties("help_button")

style help_label:
    xsize 375
    right_padding 30

style help_label_text:
    size gui.text_size
    xalign 1.0
    textalign 1.0



################################################################################
## Pantallas adicionales
################################################################################


## Pantalla de confirmación ####################################################
##
## Ren'Py llama la pantalla de confirmación para presentar al jugador preguntas
## de sí o no.
##
## https://www.renpy.org/doc/html/screen_special.html#confirm

screen confirm(message, yes_action, no_action):

    ## Asegura que otras pantallas no reciban entrada mientras se muestra esta
    ## pantalla.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 45

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 150

                textbutton _("Sí") action yes_action
                textbutton _("No") action no_action

    ## Clic derecho o escape responden "no".
    key "game_menu" action no_action


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    textalign 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.text_properties("confirm_button")


## Pantalla del indicador de salto #############################################
##
## La pantalla de indicador de salto se muestra para indicar que se está
## realizando el salto.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing 9

            text _("Saltando")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


## Esta transformación provoca el parpadeo de las flechas una tras otra.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    ## Es necesario usar un tipo de letra que contenga el glifo BLACK RIGHT-
    ## POINTING SMALL TRIANGLE.
    font "DejaVuSans.ttf"


## Pantalla de notificación ####################################################
##
## La pantalla de notificación muestra al jugador un mensaje. (Por ejemplo, con
## un guardado rápido o una captura de pantalla.)
##
## https://www.renpy.org/doc/html/screen_special.html#notify-screen

screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text "[message!tq]"

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    properties gui.text_properties("notify")


## Pantalla NVL ################################################################
##
## Esta pantalla se usa para el diálogo y los menús en modo NVL.
##
## https://www.renpy.org/doc/html/screen_special.html#nvl


screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            spacing gui.nvl_spacing

        ## Presenta el diálogo en una 'vpgrid' o una 'vbox'.
        if gui.nvl_height:

            vpgrid:
                cols 1
                yinitial 1.0

                use nvl_dialogue(dialogue)

        else:

            use nvl_dialogue(dialogue)

        ## Presenta el menú, si lo hay. El menú puede ser presentado
        ## incorrectamente si 'config.narrator_menu' está ajustado a 'True'.
        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id


## Esto controla el número máximo de entradas en modo NVL que pueden ser
## mostradas de una vez.
define config.nvl_list_length = gui.nvl_list_length

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    textalign gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    textalign gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    textalign gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.text_properties("nvl_button")


## Pantalla de globos ##########################################################
##
## La pantalla de burbujas se utiliza para mostrar el diálogo al jugador cuando
## se utilizan burbujas de diálogo. La pantalla de burbujas toma los mismos
## parámetros que la pantalla "say", debe crear un visualizable con el id de
## "what", y puede crear visualizables con los ids "namebox", "who", y "window".
##
## https://www.renpy.org/doc/html/bubble.html#bubble-screen

screen bubble(who, what):
    style_prefix "bubble"

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "bubble_namebox"

                text who:
                    id "who"

        text what:
            id "what"

        default ctc = None
        showif ctc:
            add ctc

style bubble_window is empty
style bubble_namebox is empty
style bubble_who is default
style bubble_what is default

style bubble_window:
    xpadding 30
    top_padding 5
    bottom_padding 5

style bubble_namebox:
    xalign 0.5

style bubble_who:
    xalign 0.5
    textalign 0.5
    color "#000"

style bubble_what:
    align (0.5, 0.5)
    text_align 0.5
    layout "subtitle"
    color "#000"

define bubble.frame = Frame("gui/bubble.png", 55, 55, 55, 95)
define bubble.thoughtframe = Frame("gui/thoughtbubble.png", 55, 55, 55, 55)

define bubble.properties = {
    "bottom_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "bottom_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "top_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "top_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "thought" : {
        "window_background" : bubble.thoughtframe,
    }
}

define bubble.expand_area = {
    "bottom_left" : (0, 0, 0, 22),
    "bottom_right" : (0, 0, 0, 22),
    "top_left" : (0, 22, 0, 0),
    "top_right" : (0, 22, 0, 0),
    "thought" : (0, 0, 0, 0),
}



################################################################################
## Variantes móviles
################################################################################

style pref_vbox:
    variant "medium"
    xsize 675

## Ya que puede carecer de ratón, se reempleza el menú rápido con una versión
## con menos botones y más grandes, más fáciles de tocar.
screen quick_menu():
    variant "touch"

    zorder 100

    if quick_menu:

        hbox:
            style "quick_menu"
            style_prefix "quick"

            textbutton _("Atrás") action Rollback()
            textbutton _("Saltar") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Menú") action ShowMenu()


style window:
    variant "small"
    background "gui/phone/textbox.png"

style radio_button:
    variant "small"
    foreground "gui/phone/button/radio_[prefix_]foreground.png"

style check_button:
    variant "small"
    foreground "gui/phone/button/check_[prefix_]foreground.png"

style nvl_window:
    variant "small"
    background "gui/phone/nvl.png"

style main_menu_frame:
    variant "small"
    background "gui/phone/overlay/main_menu.png"

style game_menu_outer_frame:
    variant "small"
    background "gui/phone/overlay/game_menu.png"

style game_menu_navigation_frame:
    variant "small"
    xsize 510

style game_menu_content_frame:
    variant "small"
    top_margin 0

style game_menu_viewport:
    variant "small"
    xsize 1305

style pref_vbox:
    variant "small"
    xsize 600

style bar:
    variant "small"
    ysize gui.bar_size
    left_bar Frame("gui/phone/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/phone/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    variant "small"
    xsize gui.bar_size
    top_bar Frame("gui/phone/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/phone/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    variant "small"
    ysize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    variant "small"
    xsize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    variant "small"
    ysize gui.slider_size
    base_bar Frame("gui/phone/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/horizontal_[prefix_]thumb.png"

style vslider:
    variant "small"
    xsize gui.slider_size
    base_bar Frame("gui/phone/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/vertical_[prefix_]thumb.png"

style slider_vbox:
    variant "small"
    xsize None

style slider_slider:
    variant "small"
    xsize 900
