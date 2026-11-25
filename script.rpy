init python:
    import os
    import subprocess
    import platform
    import json
    import shutil

    # Variables globales
    archivos_cargados = []  # Lista de dicts: {"nombre": ..., "tipo": ..., "contenido": ...}
    papelera = []           # Nombres de archivos movidos a la papelera
    visor_archivo_actual = None

    def registrar_archivo_web(nombre, tipo, contenido):
        """Guarda un archivo subido desde el navegador y refresca la interfaz."""
        global archivos_cargados
        if not nombre:
            return
        archivos_cargados[:] = [a for a in archivos_cargados if a.get("nombre") != nombre]
        if nombre in papelera:
            papelera.remove(nombre)
        archivos_cargados.append({
            "nombre": nombre,
            "tipo": tipo,
            "contenido": contenido
        })
        renpy.notify("¡Archivo '" + str(nombre) + "' cargado!")
        renpy.restart_interaction()

    def _consumir_subida_web():
        """Recoge de forma segura el archivo leído por JavaScript en el navegador."""
        if not getattr(renpy, 'emscripten', False):
            return
        try:
            import emscripten
            raw = emscripten.run_script("""
                (function() {
                    if (!window._archivoSubidoWeb) return "";
                    var payload = JSON.stringify(window._archivoSubidoWeb);
                    window._archivoSubidoWeb = null;
                    return payload;
                })();
            """)
            if raw:
                datos = json.loads(raw)
                if isinstance(datos, dict) and datos.get("nombre"):
                    registrar_archivo_web(
                        datos.get("nombre"),
                        datos.get("tipo", "texto"),
                        datos.get("contenido", "")
                    )
        except Exception:
            pass

    if _consumir_subida_web not in config.periodic_callbacks:
        config.periodic_callbacks.append(_consumir_subida_web)

    def subir_archivo_multimedia():
        es_web = getattr(renpy, 'emscripten', False)

        if es_web:
            import emscripten
            emscripten.run_script("""
                (function() {
                    var input = document.createElement('input');
                    input.type = 'file';
                    input.accept = '.txt,.rpy,.png,.jpg,.jpeg,.gif,.mp4,.webm,.ogg';

                    input.onchange = function(e) {
                        var file = e.target.files && e.target.files[0];
                        if (!file) return;

                        var ext = file.name.split('.').pop().toLowerCase();
                        var reader = new FileReader();

                        if (['txt', 'rpy'].indexOf(ext) !== -1) {
                            reader.onload = function(ev) {
                                window._archivoSubidoWeb = {
                                    nombre: file.name,
                                    tipo: 'texto',
                                    contenido: String(ev.target.result || '')
                                };
                            };
                            reader.readAsText(file, 'UTF-8');
                        } else {
                            reader.onload = function(ev) {
                                var tipo = (['mp4', 'webm', 'ogg'].indexOf(ext) !== -1) ? 'video' : 'imagen';
                                window._archivoSubidoWeb = {
                                    nombre: file.name,
                                    tipo: tipo,
                                    contenido: String(ev.target.result || '')
                                };
                            };
                            reader.readAsDataURL(file);
                        }
                    };

                    input.click();
                })();
            """)
        else:
            try:
                ruta_historias = os.path.join(config.gamedir, "historias")
                if not os.path.exists(ruta_historias):
                    os.makedirs(ruta_historias)

                if platform.system() == "Windows":
                    cmd = (
                        'Add-Type -AssemblyName System.Windows.Forms; '
                        '$f = New-Object System.Windows.Forms.OpenFileDialog; '
                        '$f.Filter = "Todos los permitidos (*.png;*.jpg;*.jpeg;*.mp4;*.webm;*.rpy;*.txt;*.pdf;*.doc;*.docx)|*.png;*.jpg;*.jpeg;*.mp4;*.webm;*.rpy;*.txt;*.pdf;*.doc;*.docx|Todos (*.*)|*.*"; '
                        '$f.ShowDialog() | Out-Null; $f.FileName'
                    )
                    resultado = subprocess.check_output(["powershell", "-Command", cmd]).decode('utf-8', errors='ignore').strip()
                    if resultado and os.path.exists(resultado):
                        nombre = os.path.basename(resultado)
                        destino = os.path.join(ruta_historias, nombre)
                        shutil.copy(resultado, destino)
                        ext = os.path.splitext(nombre)[1].lower()
                        tipo = "imagen" if ext in ['.png', '.jpg', '.jpeg', '.gif'] else ("texto" if ext in ['.txt', '.rpy', '.log', '.json'] else "local")
                        archivos_cargados[:] = [a for a in archivos_cargados if a.get("nombre") != nombre]
                        archivos_cargados.append({"nombre": nombre, "tipo": tipo, "contenido": destino})
                        renpy.notify("¡Archivo cargado correctamente!")
            except Exception:
                renpy.notify("Error al abrir explorador de archivos.")

        renpy.restart_interaction()

    def buscar_item_cargado(nombre):
        for item in archivos_cargados:
            if item.get("nombre") == nombre:
                return item
        return None

    def abrir_archivo(nombre):
        global visor_archivo_actual
        item = buscar_item_cargado(nombre)
        ext = os.path.splitext(nombre)[1].lower()

        # 1. Si viene subido desde Web (contenido en memoria)
        if item is not None and isinstance(item.get("contenido"), str) and (
            item["contenido"].startswith("data:") or item.get("tipo") == "texto"
        ):
            if item.get("tipo") == "imagen" or item["contenido"].startswith("data:image"):
                visor_archivo_actual = item["contenido"]
                renpy.show_screen("visor_imagenes")
                renpy.restart_interaction()
                return
            elif item.get("tipo") == "texto" or ext in ['.txt', '.rpy', '.log', '.json']:
                visor_archivo_actual = item["contenido"]
                renpy.show_screen("visor_texto", titulo=nombre, contenido=visor_archivo_actual)
                renpy.restart_interaction()
                return

        # 2. Ruta local en carpeta historias (PC / escritorio)
        ruta_completa = os.path.join(config.gamedir, "historias", nombre)

        if ext in ['.png', '.jpg', '.jpeg', '.gif']:
            visor_archivo_actual = "historias/" + nombre
            renpy.show_screen("visor_imagenes")
            renpy.restart_interaction()

        elif ext in ['.txt', '.rpy', '.log', '.json']:
            if os.path.exists(ruta_completa):
                try:
                    with open(ruta_completa, 'r', encoding='utf-8-sig', errors='replace') as f:
                        contenido = f.read()
                except Exception as e:
                    contenido = "Error al abrir el texto: " + str(e)

                visor_archivo_actual = contenido
                renpy.show_screen("visor_texto", titulo=nombre, contenido=visor_archivo_actual)
                renpy.restart_interaction()

        else:
            if os.path.exists(ruta_completa):
                try:
                    if platform.system() == "Windows":
                        os.startfile(ruta_completa)
                    elif platform.system() == "Darwin":
                        subprocess.call(["open", ruta_completa])
                    else:
                        subprocess.call(["xdg-open", ruta_completa])
                except Exception:
                    renpy.notify("No se pudo abrir el archivo externamente.")

    def obtener_historias():
        nombres = [
            item["nombre"] for item in archivos_cargados
            if item.get("nombre") not in papelera
        ]
        ruta_historias = os.path.join(config.gamedir, "historias")
        if os.path.exists(ruta_historias):
            exts = ('.txt', '.rpy', '.png', '.jpg', '.jpeg', '.mp4', '.webm')
            for f in os.listdir(ruta_historias):
                if f.lower().endswith(exts) and f not in nombres and f not in papelera:
                    nombres.append(f)
        return nombres

    def mover_a_papelera(nombre_archivo):
        global papelera
        if nombre_archivo not in papelera:
            papelera.append(nombre_archivo)
            renpy.notify("Movid@ '" + str(nombre_archivo) + "' a la Papelera.")
        renpy.restart_interaction()

    def vaciar_papelera():
        global papelera, archivos_cargados
        ruta_historias = os.path.join(config.gamedir, "historias")

        for nombre in papelera:
            archivos_cargados[:] = [
                item for item in archivos_cargados
                if item.get("nombre") != nombre
            ]

            archivo_path = os.path.join(ruta_historias, nombre)
            if os.path.exists(archivo_path):
                try:
                    os.remove(archivo_path)
                except Exception:
                    pass

        papelera.clear()
        renpy.notify("Papelera vaciada por completo.")
        renpy.restart_interaction()

    def elemento_soltado_en_papelera(drags, drop):
        if drop is not None and drop.drag_name == "papelera":
            archivo_arrastrado = drags[0].drag_name
            mover_a_papelera(archivo_arrastrado)


label procesar_subida_web(nombre, tipo, contenido):
    $ registrar_archivo_web(nombre, tipo, contenido)
    return
# -------------------------------------------------------------
# FORZAR TAMAÑO Y ORIENTACIÓN HORIZONTAL
# -------------------------------------------------------------
image bg escena1 = Transform("gui/foto1.jpg", rotate=270, align=(0.5, 0.5), anchor=(0.5, 0.5))
image bg escena2 = Transform("gui/foto2.jpg", rotate=270, align=(0.5, 0.5), anchor=(0.5, 0.5))
image bg escena3 = Transform("gui/foto3.jpg", rotate=270, align=(0.5, 0.5), anchor=(0.5, 0.5))
image bg escena4 = Transform("gui/foto4.jpg", rotate=270, align=(0.5, 0.5), anchor=(0.5, 0.5))
image bg escena5 = Transform("gui/foto5.jpg", rotate=270,  align=(0.5, 0.5), anchor=(0.5, 0.5))
image bg carteles_busqueda = Transform("gui/carteles_busqueda.jpg", size=(1920, 1080),  align=(0.5, 0.5), anchor=(0.5, 0.5))
image bg arresto_pasillo = Transform("gui/arresto_pasillo.jpg", size=(1920, 1080), align=(0.5, 0.5), anchor=(0.5, 0.5))
image bg arresto_rostro = Transform("gui/arresto_rostro.jpg",  size=(1920, 1080), align=(0.5, 0.5), anchor=(0.5, 0.5))
image bg habitacion = Transform("gui/habitacion.jpg",  size=(1920, 1080), align=(0.5, 0.5), anchor=(0.5, 0.5))
# Definición de Fondos/Imágenes
image bg entrevista_plano_general = Transform ("gui/entrevista_general.jpg", size=(1920, 1080),  align=(0.5, 0.5), anchor=(0.5, 0.5))
image bg entrevista_primer_plano = Transform("gui/entrevista_primer_plano.jpg", size=(1920, 1080),  align=(0.5, 0.5), anchor=(0.5, 0.5))
image bg entrevista_oscura = Transform("gui/entrevista_oscura.jpg", size=(1920, 1080),  align=(0.5, 0.5), anchor=(0.5, 0.5))
image bg fotos_victimas = Transform("gui/victimas_mural.jpg", size=(1920, 1080),  align=(0.5, 0.5), anchor=(0.5, 0.5))
image bg entrevista = Transform("gui/entrevista.jpg", size=(1920, 1080),  align=(0.5, 0.5), anchor=(0.5, 0.5))
define gui.sirenas = "gui/sirenas.mp3"
define gui.telefono = "gui/telefono.mp3"
# -------------------------------------------------------------
# DEFINICIÓN DE PERSONAJES
# -------------------------------------------------------------
define vecina = Character("Vecina Glenda", color="#ffcc66")
define Jeffery = Character("Jeff", color="#ff6666")
define operador = Character("Operador 911", color="#66ccff")
define i = Character("Entrevistadora", color="#ffffff")
define d = Character("Jeffrey Dahmer", color="#cf3232")

# -------------------------------------------------------------
# ETIQUETA INICIAL OBLIGATORIA
# -------------------------------------------------------------
label start:
    jump caso_dahmer_inicio

# -------------------------------------------------------------
# FLUJO DE LA NOVELA VISUAL
# -------------------------------------------------------------
label caso_dahmer_inicio:

    # 1. Foto 1: Marcando a la policía
    scene bg escena1
    with fade
    play sound "gui/telefono.mp3"
    $ renpy.pause(0.8, hard=True)

    "*(Suena el tono caracteristico de un telefono marcando rapidamente a la linea de emergencias...)*"

    # 2. Foto 2: Entra la llamada
    scene bg escena2
    with dissolve

    operador "911, ¿cual es su emergencia?"

    vecina "Por favor, necesitan enviar a alguien al edificio de apartamentos de la avenida North 25th."

    vecina "Es sobre mi vecino... Se comporta de forma extremadamente extraña a altas horas de la noche."

    # 3. Foto 3: Muestra la imagen de Jeff Dahmer (Apto. 213)
    scene bg escena3
    with dissolve

    vecina "Se llama Jeffrey. Entra y sale a horas muy raras con bolsas grandes... y ruidos extraños salen del apartamento 213."

    # 4. Foto 4: Habla de los olores raros
    scene bg escena4
    with dissolve

    vecina "Pero lo peor no es eso... Hay un olor insoportable saliendo del conducto de ventilacion de su apartamento."

    vecina "Huele a carne podrida o a algo quimico muy fuerte. ¡Ya no se puede respirar en este pasillo!"

    # 5. Toma de decisiones
    menu:
        "¿Como responde el operador del 911?"

        "Creerle a la vecina y enviar una patrulla a investigar":
            jump ruta_policia_investiga

        "Ignorar el reporte pensando que es un conflicto menor":
            jump ruta_policia_ignora


# -------------------------------------------------------------
# DESENLACES DE LA ELECCIÓN
# -------------------------------------------------------------
label ruta_policia_investiga:
    scene bg escena4
    with dissolve

    operador "Entendido, señora. Mantenga la calma, enviaremos una unidad al apartamento 213 inmediatamente."

    vecina "Gracias... por favor dense prisa."

    scene bg escena5
    with dissolve

    "*(La patrulla ha sido despachada hacia el edificio. Se inicia la investigacion...)*"

    # --- PANTALLA EN NEGRO, AUDIO Y CARGA ---
    scene black with fade
    play sound "gui/sirenas.mp3" # Audio de las sirenas en MP3

    show text "Cargando." at truecenter
    $ renpy.pause(0.8, hard=True)
    show text "Cargando.." at truecenter
    $ renpy.pause(0.8, hard=True)
    show text "Cargando..." at truecenter
    $ renpy.pause(0.8, hard=True)
    hide text with dissolve

    jump cap_2_captura


label cap_2_captura:
    # --- PRIMERA IMAGEN NUEVA: PASILLO DEL ARRESTO ---
    scene bg arresto_pasillo at truecenter with dissolve

    "La llamada a la policia rompio el ciclo..."

    "Los oficiales ingresaron al apartamento 213, descubriendo una escena grotesca y las abrumadoras evidencias acumuladas en el lugar."

    scene bg habitacion at truecenter with dissolve
    $ renpy.pause(0.8, hard=True)

    # --- SEGUNDA IMAGEN NUEVA: ROSTRO DE CERCA ---
    scene bg arresto_rostro at truecenter with dissolve

    Jeffery "Por primera vez en mucho tiempo... el silencio se volvio ensordecedor."

    Jeffery "No dije nada. No habia nada mas que explicar."

    # --- PANTALLA DE CARGA FINAL Y ENTREVISTA ---
    scene black with fade
    show text "Cargando." at truecenter
    $ renpy.pause(0.8, hard=True)
    show text "Cargando.." at truecenter
    $ renpy.pause(0.8, hard=True)
    show text "Cargando..." at truecenter
    $ renpy.pause(0.8, hard=True)
    hide text with dissolve

    jump escena_entrevista


label escena_entrevista:

    # Inicio: Plano general de la sala de entrevista
    scene bg entrevista_plano_general with dissolve

    i "Estamos en la prision de Columbia. Frente a mi se encuentra uno de los criminales más notorios..."

    i "Gracias por acceder a responder nuestras preguntas, Jeffrey."

    d "No hay problema. Solo quiero que la gente entienda que paso."

    # --- PREGUNTA 1 ---
    menu:
        i "¿Que te dirias a ti misma al comenzar?"

        "¿Cuando sentiste que perdiste el control de tus acciones?":
            jump pregunta_control

        "¿Por que decidiste conservar recuerdos de tus victimas?":
            jump pregunta_victimas


label pregunta_control:
    # Transición al plano medio/cercano de Dahmer
    scene bg entrevista_primer_plano with dissolve

    i "¿Cuando sentiste que perdiste el control por completo?"

    d "Fue un proceso gradual. Al principio eran solo fantasias... pero con el tiempo, la realidad ya no era suficiente."

    d "Sentia una necesidad obsesiva de controlar a las personas, de evitar que me dejaran."

    jump pregunta_2


label pregunta_victimas:
    # Transición a la foto del mural de víctimas
    scene bg fotos_victimas with dissolve

    i "¿Por que decidiste conservar pertenencias y fotografias de las victimas?"

    d "No queria que se fueran. Para mi... era la unica forma de mantenerlos conmigo para siempre."

    scene bg entrevista_primer_plano with dissolve

    d "Se que suena irracional, pero en ese momento tenia todo el sentido en mi cabeza."

    jump pregunta_2


label pregunta_2:

    # --- PREGUNTA 2 ---
    menu:
        i "Siguiente pregunta:"

        "¿Sentiste algun tipo de remordimiento en ese momento?":
            jump respuesta_remordimiento

        "¿Crees que habia alguna forma de haberte detenido antes?":
            jump respuesta_detener


label respuesta_remordimiento:
    # Cambio a la imagen más oscura/tenebrosa
    scene bg entrevista_oscura with dissolve

    d "En ese momento no. Estaba completamente insensibilizado."

    d "El deseo sofocaba cualquier remordimiento que pudiera sentir."

    jump pregunta_3


label respuesta_detener:
    scene bg entrevista with dissolve

    d "Tal vez si alguien hubiera notado las señales antes..."

    d "Pero la verdad es que yo mismo me aisle por completo del mundo exterior."

    jump pregunta_3


label pregunta_3:

    # --- PREGUNTA 3 (CIERRE DE LA ENTREVISTA) ---
    scene bg fotos_victimas with dissolve

    i "Hoy en dia, las familias de las victimas siguen buscando respuestas."

    scene bg entrevista_oscura with dissolve

    d "Se el dolor que cause... y no espero que nadie me perdone."

    i "Con esto concluimos la sesion de registro."

    # --- PANTALLA DE CARGA FINAL Y REINICIO ---
    scene black with fade
    show text "Cargando." at truecenter
    $ renpy.pause(0.8, hard=True)
    show text "Cargando.." at truecenter
    $ renpy.pause(0.8, hard=True)
    show text "Cargando..." at truecenter
    $ renpy.pause(0.8, hard=True)
    hide text with dissolve

    $ renpy.full_restart()


label ruta_policia_ignora:
    scene bg escena4
    with dissolve

    operador "Señora, no podemos enviar una patrulla solo por malos olores. Hable con la administración del edificio."

    vecina "¡Pero les digo que algo terrible esta pasando ahi adentro!"

    scene bg escena5
    with dissolve

    "*(El operador cuelga la llamada. La oportunidad de detenerlo antes se ha perdido...)*"

    jump transicion_carga


label transicion_carga:

    scene black with fade

    # Parpadeo de carga
    show text "Cargando." at truecenter
    $ renpy.pause(0.5, hard=True)

    show text "Cargando.." at truecenter
    $ renpy.pause(0.5, hard=True)

    show text "Cargando..." at truecenter
    $ renpy.pause(0.5, hard=True)

    hide text with dissolve

    # Siguiente imagen
    scene bg escena2 at truecenter with dissolve

    jump final_malo_dahmer


label final_malo_dahmer:

    scene black with fade
    $ renpy.pause(1.0, hard=True)

    # Muestra la foto de los carteles de búsqueda
    scene bg carteles_busqueda at truecenter with dissolve
    $ renpy.pause(2.5, hard=True)

    # Pantalla en negro dramática
    scene black with fade
    $ renpy.pause(0.8, hard=True)

    # Mensaje final en rojo
    show text "{size=45}{color=#cc2b2b}Él fue más astuto que tú.{/color}{/size}" at truecenter with dissolve
    $ renpy.pause(3.5, hard=True)

    hide text with dissolve
    $ renpy.pause(1.0, hard=True)

    # Devuelve al jugador al Menú Principal
    $ renpy.full_restart()