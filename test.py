#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import random
import subprocess
import time
from typing import Any, Iterator, NamedTuple, Optional, Union

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

import gi
gi.require_version('Atspi', '2.0')
from gi.repository import Atspi


def tree_walk(obj: Atspi.Object) -> Iterator[Atspi.Object]:
    yield obj
    for i in range(obj.get_child_count()):
        yield from tree_walk(obj.get_child_at_index(i))


#-------------------------------------------------------------------------------
# Primer test
#-------------------------------------------------------------------------------

# GIVEN he lanzado la aplicación

## Ejecuto la aplicación en un proceso del S.O.
path = "./ipm-p1.py"
name = f"{path}-test-{str(random.randint(0, 100000000))}"
process = subprocess.Popen([path, '--name', name])
assert process is not None, f"No pude ejecuar la aplicación {path}"

## Espero hasta que la aplicación aparezca en el escritorio
## Pasado un timeout abandono la espera
desktop = Atspi.get_desktop(0)
start = time.time()
timeout = 5
app = None
while app is None and (time.time() - start) < timeout:
    gen = filter(lambda child: child and child.get_name() == name,
                 (desktop.get_child_at_index(i) for i in range(desktop.get_child_count())))
    app = next(gen, None)
    if app is None:
        time.sleep(2)

## Compruebo que todo fue bien
if app is None:
    process and process.kill()
    assert False, f"La aplicación {path} no aparece en el escritorio"

    # THEN veo la vista search

## Busco el texto vacío
for obj in tree_walk(app):
    if (obj.get_role_name() == 'text' and
        obj.get_text(0, -1) == ("")):
        break
else:
    assert False, "No pude encontrar el texto 'vacio ...'"
    
## Busco el label Covid
for obj in tree_walk(app):
    if (obj.get_role_name() == 'label' and
        obj.get_text(0, -1).startswith("Covid")):
        break
else:
    assert False, "No pude encontrar la etiqueta Covid'"

    ## Compruebo el contenido
assert obj.get_text(0, -1) == "CovidTracker"

# TERMINO EL TEST DEJANDO TODO COMO ESTABA
process and process.kill()


#-------------------------------------------------------------------------------
# Segundo test
#-------------------------------------------------------------------------------

# GIVEN he lanzado la aplicación

## Ejecuto la aplicación en un proceso del S.O.
path = "./ipm-p1.py"
name = f"{path}-test-{str(random.randint(0, 100000000))}"
process = subprocess.Popen([path, '--name', name])
assert process is not None, f"No pude ejecuar la aplicación {path}"

## Espero hasta que la aplicación aparezca en el escritorio
## Pasado un timeout abandono la espera
desktop = Atspi.get_desktop(0)
start = time.time()
timeout = 5
app = None
while app is None and (time.time() - start) < timeout:
    gen = filter(lambda child: child and child.get_name() == name,
                 (desktop.get_child_at_index(i) for i in range(desktop.get_child_count())))
    app = next(gen, None)
    if app is None:
        time.sleep(2)

## Compruebo que todo fue bien
if app is None:
    process and process.kill()
    assert False, f"La aplicación {path} no aparece en el escritorio"

    
# WHEN pulso el botón 'Buscar'

## Busco el botón
for obj in tree_walk(app):
    if (obj.get_role_name() == 'push button' and
        obj.get_name() == 'Buscar'):
        break
else:
    assert False, "No pude encontrar el botón 'Buscar'"

## Busco al acción 'click' en el botón
for idx in range(obj.get_n_actions()):
    if obj.get_action_name(idx) == 'click':
        break
else:
    assert False, "El botón 'Buscar' no tiene una acción 'click'"    

## Lanzo la acción
obj.do_action(idx)
time.sleep(1)


## Busco el label Dialogo
for obj in tree_walk(app):
    if (obj.get_role_name() == 'label' and
        obj.get_text(0, -1).startswith("¡Los datos")):
        break
else:
    assert False, "No pude encontrar la etiqueta Dialogo'"

    ## Compruebo el contenido
assert obj.get_text(0, -1) == "¡Los datos introducidos no son válidos, o no se ha encontrado nadie a quien corresponda en la base de datos!"


# WHEN pulso el botón 'Close'
for obj in tree_walk(app):
    if (obj.get_role_name() == 'push button' and
        obj.get_name() == 'Close'):
        break
else:
    assert False, "No pude encontrar el botón 'Close'"

## Busco al acción 'click' en el botón
for idx in range(obj.get_n_actions()):
    if obj.get_action_name(idx) == 'click':
        break
else:
    assert False, "El botón 'Close' no tiene una acción 'click'"    

## Lanzo la acción
obj.do_action(idx)
time.sleep(1)

process and process.kill()

# -------------------------------------------------------------------------------
# Segundo test (Persona que no existe)
# -------------------------------------------------------------------------------

# GIVEN he lanzado la aplicación

## Ejecuto la aplicación en un proceso del S.O.
path = "./ipm-p1.py"
name = f"{path}-test-{str(random.randint(0, 100000000))}"
process = subprocess.Popen([path, '--name', name])
assert process is not None, f"No pude ejecuar la aplicación {path}"

## Espero hasta que la aplicación aparezca en el escritorio
## Pasado un timeout abandono la espera
desktop = Atspi.get_desktop(0)
start = time.time()
timeout = 5
app = None
while app is None and (time.time() - start) < timeout:
    gen = filter(lambda child: child and child.get_name() == name,
                 (desktop.get_child_at_index(i) for i in range(desktop.get_child_count())))
    app = next(gen, None)
    if app is None:
        time.sleep(2)

## Compruebo que todo fue bien
if app is None:
    process and process.kill()
    assert False, f"La aplicación {path} no aparece en el escritorio"

## Cambio el nombre
for obj in tree_walk(app):
    if (obj.get_role_name() == 'text' and
        obj.get_text(0, -1) == ("")):
        obj.set_text_contents('Juan Torres')
        break
else:
    assert False, "No pude encontrar el Nombre'"

# WHEN pulso el botón 'Buscar'

## Busco el botón
for obj in tree_walk(app):
    if (obj.get_role_name() == 'push button' and
            obj.get_name() == 'Buscar'):
        break
else:
    assert False, "No pude encontrar el botón 'Buscar'"

## Busco al acción 'click' en el botón
for idx in range(obj.get_n_actions()):
    if obj.get_action_name(idx) == 'click':
        break
else:
    assert False, "El botón 'Buscar' no tiene una acción 'click'"

## Lanzo la acción
obj.do_action(idx)
time.sleep(1)

## Busco el label Dialogo
for obj in tree_walk(app):
    if (obj.get_role_name() == 'label' and
            obj.get_text(0, -1).startswith("¡Los datos")):
        break
else:
    assert False, "No pude encontrar la etiqueta Dialogo'"

    ## Compruebo el contenido
assert obj.get_text(0,
                    -1) == "¡Los datos introducidos no son válidos, o no se ha encontrado nadie a quien corresponda en la base de datos!"

# WHEN pulso el botón 'Close'
for obj in tree_walk(app):
    if (obj.get_role_name() == 'push button' and
            obj.get_name() == 'Close'):
        break
else:
    assert False, "No pude encontrar el botón 'Close'"

## Busco al acción 'click' en el botón
for idx in range(obj.get_n_actions()):
    if obj.get_action_name(idx) == 'click':
        break
else:
    assert False, "El botón 'Close' no tiene una acción 'click'"

## Lanzo la acción
obj.do_action(idx)
time.sleep(1)

process and process.kill()


#-------------------------------------------------------------------------------
# Tercer test
#-------------------------------------------------------------------------------

# GIVEN he lanzado la aplicación

## Ejecuto la aplicación en un proceso del S.O.
path = "./ipm-p1.py"
name = f"{path}-test-{str(random.randint(0, 100000000))}"
process = subprocess.Popen([path, '--name', name])
assert process is not None, f"No pude ejecuar la aplicación {path}"

## Espero hasta que la aplicación aparezca en el escritorio
## Pasado un timeout abandono la espera
desktop = Atspi.get_desktop(0)
start = time.time()
timeout = 5
app = None
while app is None and (time.time() - start) < timeout:
    gen = filter(lambda child: child and child.get_name() == name,
                 (desktop.get_child_at_index(i) for i in range(desktop.get_child_count())))
    app = next(gen, None)
    if app is None:
        time.sleep(2)

## Compruebo que todo fue bien
if app is None:
    process and process.kill()
    assert False, f"La aplicación {path} no aparece en el escritorio"


## Cambio el nombre
for obj in tree_walk(app):
    if (obj.get_role_name() == 'text' and
        obj.get_text(0, -1) == ("")):
        obj.set_text_contents('Nieves Vargas')
        break
else:
    assert False, "No pude encontrar el Nombre'"

# WHEN pulso el botón 'Buscar'
for obj in tree_walk(app):
    if (obj.get_role_name() == 'push button' and
        obj.get_name() == 'Buscar'):
        break
else:
    assert False, "No pude encontrar el botón 'Buscar'"

## Busco al acción 'click' en el botón
for idx in range(obj.get_n_actions()):
    if obj.get_action_name(idx) == 'click':
        break
else:
    assert False, "El botón 'Buscar' no tiene una acción 'click'"    

## Lanzo la acción
obj.do_action(idx)
time.sleep(1)

# THEN veo la vista Persona

## Busco el label nombre
for obj in tree_walk(app):
    if (obj.get_role_name() == 'label' and
        obj.get_text(0, -1).startswith("Nombre:")):
        break
else:
    assert False, "No pude encontrar la etiqueta Nombre:"

## Busco el label nombre de la persona
for obj in tree_walk(app):
    if (obj.get_role_name() == 'label' and
        obj.get_text(0, -1).startswith("Nieves")):
        break
else:
    assert False, "No pude encontrar la etiqueta Nieves"

## Compruebo el contenido
assert obj.get_text(0, -1) == "Nieves"

## Busco el label Apellidos
for obj in tree_walk(app):
    if (obj.get_role_name() == 'label' and
        obj.get_text(0, -1).startswith("Apellidos:")):
        break
else:
    assert False, "No pude encontrar la etiqueta Apellidos:"

## Compruebo el contenido
assert obj.get_text(0, -1) == "Apellidos:"

## Busco el label apellido de la persona
for obj in tree_walk(app):
    if (obj.get_role_name() == 'label' and
        obj.get_text(0, -1).startswith("Vargas")):
        break
else:
    assert False, "No pude encontrar la etiqueta Vargas"

## Compruebo el contenido
assert obj.get_text(0, -1) == "Vargas"

## Busco el label nombre de usuario
for obj in tree_walk(app):
    if (obj.get_role_name() == 'label' and
        obj.get_text(0, -1).startswith("Nombre de usuario:")):
        break
else:
    assert False, "No pude encontrar la etiqueta nombre de usuario:"
## Compruebo el contenido
assert obj.get_text(0, -1) == "Nombre de usuario:"

## Busco el label nombre de la usuario
for obj in tree_walk(app):
    if (obj.get_role_name() == 'label' and
        obj.get_text(0, -1).startswith("sadsnake479")):
        break
else:
    assert False, "No pude encontrar la etiqueta sadsnake479"

## Compruebo el contenido
assert obj.get_text(0, -1) == "sadsnake479"

for obj in tree_walk(app):
    if (obj.get_role_name() == 'label' and
        obj.get_text(0, -1).startswith("Correo")):
        break
else:
    assert False, "No pude encontrar la etiqueta Apellidos:"
## Compruebo el contenido
assert obj.get_text(0, -1) == "Correo electrónico:"

## Busco el label correo de la persona
for obj in tree_walk(app):
    if (obj.get_role_name() == 'label' and
        obj.get_text(0, -1).startswith("nieves.vargas@example.com")):
        break
else:
    assert False, "No pude encontrar la etiqueta correo persona"

## Compruebo el contenido
assert obj.get_text(0, -1) == "nieves.vargas@example.com"

for obj in tree_walk(app):
    if (obj.get_role_name() == 'label' and
        obj.get_text(0, -1).startswith("Teléfono")):
        break
else:
    assert False, "No pude encontrar la etiqueta Telefono:"
## Compruebo el contenido
assert obj.get_text(0, -1) == "Teléfono:"

## Busco el label teléfono de la persona
for obj in tree_walk(app):
    if (obj.get_role_name() == 'label' and
        obj.get_text(0, -1).startswith("990-350-465")):
        break
else:
    assert False, "No pude encontrar la etiqueta numero"

## Compruebo el contenido
assert obj.get_text(0, -1) == "990-350-465"

for obj in tree_walk(app):
    if (obj.get_role_name() == 'label' and
        obj.get_text(0, -1).startswith("¿Vacunada?")):
        break
else:
    assert False, "No pude encontrar la etiqueta ¿Vacunada?"
## Compruebo el contenido
assert obj.get_text(0, -1) == "¿Vacunada?"

for obj in tree_walk(app):
    if (obj.get_role_name() == 'label' and
        obj.get_text(0, -1).startswith("No")):
        break
else:
    assert False, "No pude encontrar si estaba vacunada:"
## Compruebo el contenido
assert obj.get_text(0, -1) == "No"

for obj in tree_walk(app):
    if (obj.get_role_name() == 'label' and
        obj.get_text(0, -1).startswith("Identificador QR:")):
        break
else:
    assert False, "No pude encontrar la etiqueta Identificador QR"

for obj in tree_walk(app):
    if (obj.get_role_name() == 'label' and
        obj.get_text(0, -1).startswith("Accesos")):
        break
else:
    assert False, "No pude encontrar la etiqueta Accesos"
# Compruebo el contenido
assert obj.get_text(0, -1) == "Accesos recientes"

# Veo titulo de lista Temperatura
for obj in tree_walk(app):
    if (obj.get_role_name() == 'table column header' and
        obj.get_name() == 'Temperatura'):
        break
else:
    assert False, "No pude encontrar el botón 'Temperatura'"

# Veo titulo de lista Fecha/Hora
for obj in tree_walk(app):
    if (obj.get_role_name() == 'table column header' and
        obj.get_name() == 'Fecha/Hora'):
        break
else:
    assert False, "No pude encontrar el botón 'Fecha/Hora'"

# Veo titulo de lista Instalación
for obj in tree_walk(app):
    if (obj.get_role_name() == 'table column header' and
        obj.get_name() == 'Instalación'):
        break
else:
    assert False, "No pude encontrar el botón 'Instalación'"

# Veo Fecha/Hora
count=0
for obj in tree_walk(app):
    if(obj.get_role_name() == 'table column header' and
        obj.get_name() == 'Fecha/Hora' and count<1):
        count+=1
    elif (obj.get_role_name() == 'table column header' and
        obj.get_name() == 'Fecha/Hora' and count==1):
        break
else:
    assert False, "No pude encontrar la 'Fecha/Hora'"

# Veo Instalación
count=0
for obj in tree_walk(app):
    if(obj.get_role_name() == 'table column header' and
        obj.get_name() == 'Instalación' and count<1):
        count+=1
    elif (obj.get_role_name() == 'table column header' and
        obj.get_name() == 'Instalación' and count==1):
        break
else:
    assert False, "No pude encontrar la 'Instalación'"

# Veo titulo de lista Usuarios
for obj in tree_walk(app):
    if (obj.get_role_name() == 'table column header' and
        obj.get_name() == 'Usuario'):
        break
else:
    assert False, "No pude encontrar el botón 'Usuario'"

# Veo titulo de lista Apellidos
for obj in tree_walk(app):
    if (obj.get_role_name() == 'table column header' and
        obj.get_name() == 'Apellidos'):
        break
else:
    assert False, "No pude encontrar el botón 'Apellidos'"  



# TERMINO EL TEST DEJANDO TODO COMO ESTABA
process and process.kill()

#-------------------------------------------------------------------------------
# Cuarto test
#-------------------------------------------------------------------------------

# GIVEN he lanzado la aplicación

## Ejecuto la aplicación en un proceso del S.O.
path = "./ipm-p1.py"
name = f"{path}-test-{str(random.randint(0, 100000000))}"
process = subprocess.Popen([path, '--name', name])
assert process is not None, f"No pude ejecuar la aplicación {path}"

## Espero hasta que la aplicación aparezca en el escritorio
## Pasado un timeout abandono la espera
desktop = Atspi.get_desktop(0)
start = time.time()
timeout = 5
app = None
while app is None and (time.time() - start) < timeout:
    gen = filter(lambda child: child and child.get_name() == name,
                 (desktop.get_child_at_index(i) for i in range(desktop.get_child_count())))
    app = next(gen, None)
    if app is None:
        time.sleep(2)

## Compruebo que todo fue bien
if app is None:
    process and process.kill()
    assert False, f"La aplicación {path} no aparece en el escritorio"


## Cambio el nombre
for obj in tree_walk(app):
    if (obj.get_role_name() == 'text' and
        obj.get_text(0, -1) == ("")):
        obj.set_text_contents('Nieves Vargas')
        break
else:
    assert False, "No pude encontrar el Nombre'"

# WHEN pulso el botón 'Buscar'
for obj in tree_walk(app):
    if (obj.get_role_name() == 'push button' and
        obj.get_name() == 'Buscar'):
        break
else:
    assert False, "No pude encontrar el botón 'Buscar'"


## Busco al acción 'click' en el botón
for idx in range(obj.get_n_actions()):
    if obj.get_action_name(idx) == 'click':
        break
else:
    assert False, "El botón 'Buscar' no tiene una acción 'click'"

## Lanzo la acción
obj.do_action(idx)
time.sleep(1)

# WHEN pulso el botón 'Accesos'
for obj in tree_walk(app):
    if (obj.get_role_name() == 'push button' and
        obj.get_name() == 'Expandir accesos'):
        break
else:
    assert False, "No pude encontrar el botón 'Expandir accesos'"

## Busco al acción 'click' en el botón
for idx in range(obj.get_n_actions()):
    if obj.get_action_name(idx) == 'click':
        break
else:
    assert False, "El botón 'Expandir accesos' no tiene una acción 'click'"    

## Lanzo la acción
obj.do_action(idx)
time.sleep(1)

# Busco en el treeview el elemento 'Polideportivo Isaac Delgado'
for obj in tree_walk(app):
    if (obj.get_role_name() == 'table cell' and
        obj.get_name().startswith("Polideportivo Isaac Delgado")):
        break
else:
    assert False, "No pude encontrar la etiqueta Polideportivo Isaac Delgado"

# WHEN pulso el botón 'Forward'
for obj in tree_walk(app):
    if (obj.get_role_name() == 'push button' and
        obj.get_name() == 'Forward'):
        break
else:
    assert False, "No pude encontrar el botón 'Forward'"

## Busco al acción 'click' en el botón
for idx in range(obj.get_n_actions()):
    if obj.get_action_name(idx) == 'click':
        break
else:
    assert False, "El botón 'Forward' no tiene una acción 'click'"    

## Lanzo la acción
obj.do_action(idx)
time.sleep(2)

# Busco en el treeview el elemento 'Polideportivo Isaac Delgado'
for obj in tree_walk(app):
    if (obj.get_role_name() == 'table cell' and
        obj.get_name().startswith("Polideportivo Isaac Delgado")):
        break
else:
    assert False, "No pude encontrar la etiqueta Polideportivo Isaac Delgado"

# WHEN pulso el botón 'Back'
count=0
for obj in tree_walk(app):
    if(obj.get_role_name() == 'push button' and
        obj.get_name() == 'Back' and count<1):
        count+=1
    elif (obj.get_role_name() == 'push button' and
        obj.get_name() == 'Back' and count==1):
        break
else:
    assert False, "No pude encontrar el botón 'Back'"

## Busco al acción 'click' en el botón
for idx in range(obj.get_n_actions()):
    if obj.get_action_name(idx) == 'click':
        break
else:
    assert False, "El botón 'Back' no tiene una acción 'click'"    

## Lanzo la acción
obj.do_action(idx)
time.sleep(2)

# Busco en el treeview el elemento 'Polideportivo Isaac Delgado'
for obj in tree_walk(app):
    if (obj.get_role_name() == 'table cell' and
        obj.get_name().startswith("Polideportivo Isaac Delgado")):
        break
else:
    assert False, "No pude encontrar la etiqueta Polideportivo Isaac Delgado"

# WHEN pulso el botón 'Jump to'
count=0
for obj in tree_walk(app):
    if(obj.get_role_name() == 'text' and
        obj.get_text(0, -1) == ("0")):
        obj.set_text_contents('1')
        break
else:
    assert False, "No pude encontrar el botón 'Back'"

# WHEN pulso el botón 'Jump to'
for obj in tree_walk(app):
    if (obj.get_role_name() == 'push button' and
        obj.get_name() == 'Jump to'):
        break
else:
    assert False, "No pude encontrar el botón 'Jump to'"

## Busco al acción 'click' en el botón
for idx in range(obj.get_n_actions()):
    if obj.get_action_name(idx) == 'click':
        break
else:
    assert False, "El botón 'Jump to' no tiene una acción 'click'"    

## Lanzo la acción
obj.do_action(idx)
time.sleep(2)

# Busco en el treeview el elemento 'Polideportivo Isaac Delgado'
for obj in tree_walk(app):
    if (obj.get_role_name() == 'table cell' and
        obj.get_name().startswith("Polideportivo Isaac Delgado")):
        break
else:
    assert False, "No pude encontrar la etiqueta Polideportivo Isaac Delgado"

# WHEN pulso el botón 'Back'
for obj in tree_walk(app):
    if (obj.get_role_name() == 'push button' and
        obj.get_name() == 'Back'):
        break
else:
    assert False, "No pude encontrar el botón 'Back'"


## Busco al acción 'click' en el botón
for idx in range(obj.get_n_actions()):
    if obj.get_action_name(idx) == 'click':
        break
else:
    assert False, "El botón 'Back' no tiene una acción 'click'"    

## Lanzo la acción
obj.do_action(idx)
time.sleep(1)

# TERMINO EL TEST DEJANDO TODO COMO ESTABA
process and process.kill()

#-------------------------------------------------------------------------------
# Quinto test
#-------------------------------------------------------------------------------

# GIVEN he lanzado la aplicación

## Ejecuto la aplicación en un proceso del S.O.
path = "./ipm-p1.py"
name = f"{path}-test-{str(random.randint(0, 100000000))}"
process = subprocess.Popen([path, '--name', name])
assert process is not None, f"No pude ejecuar la aplicación {path}"

## Espero hasta que la aplicación aparezca en el escritorio
## Pasado un timeout abandono la espera
desktop = Atspi.get_desktop(0)
start = time.time()
timeout = 5
app = None
while app is None and (time.time() - start) < timeout:
    gen = filter(lambda child: child and child.get_name() == name,
                 (desktop.get_child_at_index(i) for i in range(desktop.get_child_count())))
    app = next(gen, None)
    if app is None:
        time.sleep(2)

## Compruebo que todo fue bien
if app is None:
    process and process.kill()
    assert False, f"La aplicación {path} no aparece en el escritorio"


## Cambio el nombre
for obj in tree_walk(app):
    if (obj.get_role_name() == 'text' and
        obj.get_text(0, -1) == ("")):
        obj.set_text_contents('Nieves Vargas')
        break
else:
    assert False, "No pude encontrar el Nombre'"

# WHEN pulso el botón 'Buscar'
for obj in tree_walk(app):
    if (obj.get_role_name() == 'push button' and
        obj.get_name() == 'Buscar'):
        break
else:
    assert False, "No pude encontrar el botón 'Buscar'"


## Busco al acción 'click' en el botón
for idx in range(obj.get_n_actions()):
    if obj.get_action_name(idx) == 'click':
        break
else:
    assert False, "El botón 'Buscar' no tiene una acción 'click'"

## Lanzo la acción
obj.do_action(idx)
time.sleep(1)

# WHEN pulso el botón 'Expandir contactos'
for obj in tree_walk(app):
    if (obj.get_role_name() == 'push button' and
        obj.get_name() == 'Expandir contactos'):
        break
else:
    assert False, "No pude encontrar el botón 'Expandir contactos'"

## Busco al acción 'click' en el botón
for idx in range(obj.get_n_actions()):
    if obj.get_action_name(idx) == 'click':
        break
else:
    assert False, "El botón 'Expandir contactos' no tiene una acción 'click'"    

## Lanzo la acción
obj.do_action(idx)
time.sleep(1)


# Busco en el treeview el elemento 'Javier Jimenez'
count = 0
for obj in tree_walk(app):
    if (obj.get_role_name() == 'table cell' and
            obj.get_name().startswith("Jimenez") and count==1):
        break
    if (obj.get_role_name() == 'table cell' and
            obj.get_name().startswith("Javier")):
        count=1
    else:
        count = 0
else:
    assert False, "No pude encontrar la etiqueta Javier Jimenez"

# TERMINO EL TEST DEJANDO TODO COMO ESTABA
process and process.kill()

#-------------------------------------------------------------------------------
# Sexto test
#-------------------------------------------------------------------------------

# GIVEN he lanzado la aplicación

## Ejecuto la aplicación en un proceso del S.O.
path = "./ipm-p1.py"
name = f"{path}-test-{str(random.randint(0, 100000000))}"
process = subprocess.Popen([path, '--name', name])
assert process is not None, f"No pude ejecuar la aplicación {path}"

## Espero hasta que la aplicación aparezca en el escritorio
## Pasado un timeout abandono la espera
desktop = Atspi.get_desktop(0)
start = time.time()
timeout = 7
app = None
while app is None and (time.time() - start) < timeout:
    gen = filter(lambda child: child and child.get_name() == name,
                 (desktop.get_child_at_index(i) for i in range(desktop.get_child_count())))
    app = next(gen, None)
    if app is None:
        time.sleep(2)

## Compruebo que todo fue bien
if app is None:
    process and process.kill()
    assert False, f"La aplicación {path} no aparece en el escritorio"


## Cambio el nombre
for obj in tree_walk(app):
    if (obj.get_role_name() == 'text' and
        obj.get_text(0, -1) == ("")):
        obj.set_text_contents('Nieves Vargas')
        break
else:
    assert False, "No pude encontrar el Nombre'"

# WHEN pulso el botón 'Buscar'
for obj in tree_walk(app):
    if (obj.get_role_name() == 'push button' and
        obj.get_name() == 'Buscar'):
        break
else:
    assert False, "No pude encontrar el botón 'Buscar'"


## Busco al acción 'click' en el botón
for idx in range(obj.get_n_actions()):
    if obj.get_action_name(idx) == 'click':
        break
else:
    assert False, "El botón 'Buscar' no tiene una acción 'click'"

## Lanzo la acción
obj.do_action(idx)

# THEN veo la vista Persona
time.sleep(1)

# WHEN busco el botón 'Expandir contactos'
for obj in tree_walk(app):
    if (obj.get_role_name() == 'push button' and
        obj.get_name() == 'Expandir contactos'):
        break
else:
    assert False, "No pude encontrar el botón 'Expandir contactos'"

## Busco la acción 'click' en el botón
for idx in range(obj.get_n_actions()):
    if obj.get_action_name(idx) == 'click':
        break
else:
    assert False, "El botón 'Expandir contactos' no tiene una acción 'click'"

## Lanzo la acción
obj.do_action(idx)
time.sleep(1)

# WHEN busco el botón 'Filtrar or fecha'
for obj in tree_walk(app):
    if (obj.get_role_name() == 'push button' and
        obj.get_name() == 'Filtrar por fecha'):
        break
else:
    assert False, "No pude encontrar el botón 'Filtrar por fecha'"

## Lanzo la acción
obj.do_action(idx)
time.sleep(1)

# Busco el calendario 'desde'
for obj in tree_walk(app):
    if (obj.get_role_name() == 'calendar'):
        break
else:
    assert False, "No pude encontrar el calendario 'desde'"

# Busco el calendario 'hasta'
count = 0
for obj in tree_walk(app):
    if (obj.get_role_name() == 'calendar' and count < 1):
        count+=1
    elif (obj.get_role_name() == 'calendar' and count == 1):
        break
else:
    assert False, "No pude encontrar el calendario 'hasta'"

# WHEN busco el botón 'Find'
for obj in tree_walk(app):
    if (obj.get_role_name() == 'push button' and
        obj.get_name() == 'Find'):
        break
else:
    assert False, "No pude encontrar el botón 'Find'"

## Busco la acción 'click' en el botón
for idx in range(obj.get_n_actions()):
    if obj.get_action_name(idx) == 'click':
        break
else:
    assert False, "El botón 'Find' no tiene una acción 'click'"

## Lanzo la acción
obj.do_action(idx)
time.sleep(1)

# TERMINO EL TEST DEJANDO TODO COMO ESTABA
process and process.kill()

#-------------------------------------------------------------------------------
# Séptimo test
#-------------------------------------------------------------------------------

# GIVEN he lanzado la aplicación

## Ejecuto la aplicación en un proceso del S.O.
path = "./ipm-p1.py"
name = f"{path}-test-{str(random.randint(0, 100000000))}"
process = subprocess.Popen([path, '--name', name])
assert process is not None, f"No pude ejecuar la aplicación {path}"

## Espero hasta que la aplicación aparezca en el escritorio
## Pasado un timeout abandono la espera
desktop = Atspi.get_desktop(0)
start = time.time()
timeout = 5
app = None
while app is None and (time.time() - start) < timeout:
    gen = filter(lambda child: child and child.get_name() == name,
                 (desktop.get_child_at_index(i) for i in range(desktop.get_child_count())))
    app = next(gen, None)
    if app is None:
        time.sleep(2)

## Compruebo que todo fue bien
if app is None:
    process and process.kill()
    assert False, f"La aplicación {path} no aparece en el escritorio"

    
## Busco el botón
for obj in tree_walk(app):
    if (obj.get_role_name() == 'text' and
        obj.get_text(0, -1) == ("")):
        obj.set_text_contents('Arturo Blanco')
        break
else:
    assert False, "No pude encontrar el Nombre'"

# WHEN pulso el botón 'Buscar'
for obj in tree_walk(app):
    if (obj.get_role_name() == 'push button' and
        obj.get_name() == 'Buscar'):
        break
else:
    assert False, "No pude encontrar el botón 'Buscar'"



## Busco al acción 'click' en el botón
for idx in range(obj.get_n_actions()):
    if obj.get_action_name(idx) == 'click':
        break
else:
    assert False, "El botón 'Buscar' no tiene una acción 'click'"    

## Lanzo la acción
obj.do_action(idx)
time.sleep(1)

##Busco Titulo Sugerencias
for obj in tree_walk(app):
    if (obj.get_role_name() == 'table column header' and
        obj.get_name() == 'Sugerencias'):
        break
else:
    assert False, "No pude encontrar el botón 'table column header'"

##Busco Nombre en Sugerencias 
for obj in tree_walk(app):
    if (obj.get_role_name() == 'table cell' and
        obj.get_text(0, -1).startswith("goldenbird345")):
        break
else:
    assert False, "No pude encontrar el botón 'table column header'"

## Busco al acción 'activate' en el botón
for idx in range(obj.get_n_actions()):
    if obj.get_action_name(idx) == 'activate':
        break
else:
    assert False, "El botón 'Sugerencias' no tiene una acción 'activated'"    

## Lanzo la acción
obj.do_action(idx)
time.sleep(1)
# THEN veo el texto "Has pulsado 4 veces"

## Busco el Nombre
for obj in tree_walk(app):
    if (obj.get_role_name() == 'label' and
        obj.get_text(0, -1).startswith("Nombre:")):
        break
else:
    assert False, "No pude encontrar la etiqueta Nombre:"

# THEN veo la vista Persona

## Busco el label nombre
for obj in tree_walk(app):
    if (obj.get_role_name() == 'label' and
        obj.get_text(0, -1).startswith("Nombre:")):
        break
else:
    assert False, "No pude encontrar la etiqueta Nombre:"

## Compruebo el contenido
assert obj.get_text(0, -1) == "Nombre:"

## Busco el label Apellidos
for obj in tree_walk(app):
    if (obj.get_role_name() == 'label' and
        obj.get_text(0, -1).startswith("Apellidos:")):
        break
else:
    assert False, "No pude encontrar la etiqueta Apellidos:"

## Compruebo el contenido
assert obj.get_text(0, -1) == "Apellidos:"

## Busco el label nombre de usuario
for obj in tree_walk(app):
    if (obj.get_role_name() == 'label' and
        obj.get_text(0, -1).startswith("Nombre de usuario:")):
        break
else:
    assert False, "No pude encontrar la etiqueta nombre de usuario:"
## Compruebo el contenido
assert obj.get_text(0, -1) == "Nombre de usuario:"

for obj in tree_walk(app):
    if (obj.get_role_name() == 'label' and
        obj.get_text(0, -1).startswith("Correo")):
        break
else:
    assert False, "No pude encontrar la etiqueta Apellidos:"
## Compruebo el contenido
assert obj.get_text(0, -1) == "Correo electrónico:"

for obj in tree_walk(app):
    if (obj.get_role_name() == 'label' and
        obj.get_text(0, -1).startswith("Teléfono")):
        break
else:
    assert False, "No pude encontrar la etiqueta Apellidos:"
## Compruebo el contenido
assert obj.get_text(0, -1) == "Teléfono:"

for obj in tree_walk(app):
    if (obj.get_role_name() == 'label' and
        obj.get_text(0, -1).startswith("¿Vacunada?")):
        break
else:
    assert False, "No pude encontrar la etiqueta ¿Vacunada?"
## Compruebo el contenido
assert obj.get_text(0, -1) == "¿Vacunada?"

for obj in tree_walk(app):
    if (obj.get_role_name() == 'label' and
        obj.get_text(0, -1).startswith("No")):
        break
else:
    assert False, "No pude encontrar si estaba vacunada:"
## Compruebo el contenido
assert obj.get_text(0, -1) == "No"

for obj in tree_walk(app):
    if (obj.get_role_name() == 'label' and
        obj.get_text(0, -1).startswith("Identificador QR:")):
        break
else:
    assert False, "No pude encontrar la etiqueta Identificador QR"

for obj in tree_walk(app):
    if (obj.get_role_name() == 'label' and
        obj.get_text(0, -1).startswith("Accesos")):
        break
else:
    assert False, "No pude encontrar la etiqueta Accesos"
# Compruebo el contenido
assert obj.get_text(0, -1) == "Accesos recientes"

for obj in tree_walk(app):
    if (obj.get_role_name() == 'label' and
        obj.get_text(0, -1).startswith("Ha")):
        break
else:
    assert False, "No pude encontrar la etiqueta Contactos"
# Compruebo el contenido
assert obj.get_text(0, -1) == "Ha estado con...."

# TERMINO EL TEST DEJANDO TODO COMO ESTABA
process and process.kill()

#-------------------------------------------------------------------------------
# Octavo test
#-------------------------------------------------------------------------------

# GIVEN he lanzado la aplicación

## Ejecuto la aplicación en un proceso del S.O.
path = "./ipm-p1.py"
name = f"{path}-test-{str(random.randint(0, 100000000))}"
process = subprocess.Popen([path, '--name', name])
assert process is not None, f"No pude ejecuar la aplicación {path}"

## Espero hasta que la aplicación aparezca en el escritorio
## Pasado un timeout abandono la espera
desktop = Atspi.get_desktop(0)
start = time.time()
timeout = 5
app = None
while app is None and (time.time() - start) < timeout:
    gen = filter(lambda child: child and child.get_name() == name,
                 (desktop.get_child_at_index(i) for i in range(desktop.get_child_count())))
    app = next(gen, None)
    if app is None:
        time.sleep(2)

## Compruebo que todo fue bien
if app is None:
    process and process.kill()
    assert False, f"La aplicación {path} no aparece en el escritorio"

# WHEN Busco el botón Home
for obj in tree_walk(app):
    if (obj.get_role_name() == 'push button' and
            obj.get_name() == 'Home'):
        break
else:
    assert False, "No pude encontrar la etiqueta Home"

# Busco al acción 'click' en el botón
for idx in range(obj.get_n_actions()):
    if obj.get_action_name(idx) == 'click':
        break
else:
    assert False, "El botón 'Home' no tiene una acción 'click'"

## Lanzo la acción
obj.do_action(idx)
time.sleep(1)

## Cambio el nombre
for obj in tree_walk(app):
    if (obj.get_role_name() == 'text' and
        (obj.get_text(0, -1) == ("") or obj.get_text(0, -1) == ("Nieves Vargas"))):
        obj.set_text_contents('Nieves Vargas')
        break
else:
    assert False, "No pude encontrar el Nombre'"

# WHEN pulso el botón 'Buscar'
for obj in tree_walk(app):
    if (obj.get_role_name() == 'push button' and
        obj.get_name() == 'Buscar'):
        break
else:
    assert False, "No pude encontrar el botón 'Buscar'"
## Busco al acción 'click' en el botón
for idx in range(obj.get_n_actions()):
    if obj.get_action_name(idx) == 'click':
        break
else:
    assert False, "El botón 'Buscar' no tiene una acción 'click'"

## Lanzo la acción
obj.do_action(idx)
time.sleep(1)

# THEN Busco el botón Home
for obj in tree_walk(app):
    if (obj.get_role_name() == 'push button' and
            obj.get_name() == 'Home'):
        break
else:
    assert False, "No pude encontrar la etiqueta Home"

# Busco al acción 'click' en el botón
for idx in range(obj.get_n_actions()):
    if obj.get_action_name(idx) == 'click':
        break
else:
    assert False, "El botón 'Home' no tiene una acción 'click'"

## Lanzo la acción
obj.do_action(idx)
time.sleep(1)

## Cambio el nombre
for obj in tree_walk(app):
    if (obj.get_role_name() == 'text' and
            (obj.get_text(0, -1) == ("") or obj.get_text(0, -1) == ("Nieves Vargas"))):
        obj.set_text_contents('Nieves Vargas')
        break
else:
    assert False, "No pude encontrar el Nombre'"

# WHEN pulso el botón 'Buscar'
for obj in tree_walk(app):
    if (obj.get_role_name() == 'push button' and
        obj.get_name() == 'Buscar'):
        break
else:
    assert False, "No pude encontrar el botón 'Buscar'"
## Busco al acción 'click' en el botón
for idx in range(obj.get_n_actions()):
    if obj.get_action_name(idx) == 'click':
        break
else:
    assert False, "El botón 'Buscar' no tiene una acción 'click'"

## Lanzo la acción
obj.do_action(idx)
time.sleep(1)

# WHEN pulso el botón 'Accesos'
for obj in tree_walk(app):
    if (obj.get_role_name() == 'push button' and
        obj.get_name() == 'Expandir accesos'):
        break
else:
    assert False, "No pude encontrar el botón 'Expandir accesos'"

## Busco al acción 'click' en el botón
for idx in range(obj.get_n_actions()):
    if obj.get_action_name(idx) == 'click':
        break
else:
    assert False, "El botón 'Expandir accesos' no tiene una acción 'click'"

## Lanzo la acción
obj.do_action(idx)
time.sleep(1)

# THEN Busco el botón Home
for obj in tree_walk(app):
    if (obj.get_role_name() == 'push button' and
            obj.get_name() == 'Home'):
        break
else:
    assert False, "No pude encontrar la etiqueta Home"

# Busco al acción 'click' en el botón
for idx in range(obj.get_n_actions()):
    if obj.get_action_name(idx) == 'click':
        break
else:
    assert False, "El botón 'Home' no tiene una acción 'click'"

## Lanzo la acción
obj.do_action(idx)
time.sleep(1)

## Cambio el nombre
for obj in tree_walk(app):
    if (obj.get_role_name() == 'text' and
            (obj.get_text(0, -1) == ("") or obj.get_text(0, -1) == ("Nieves Vargas"))):
        obj.set_text_contents('Nieves Vargas')
        break
else:
    assert False, "No pude encontrar el Nombre'"

# WHEN busco el botón 'Buscar'
for obj in tree_walk(app):
    if (obj.get_role_name() == 'push button' and
        obj.get_name() == 'Buscar'):
        break
else:
    assert False, "No pude encontrar el botón 'Buscar'"

## Lanzo la acción
obj.do_action(idx)
time.sleep(1)

# WHEN pulso el botón 'Expandir contactos'
for obj in tree_walk(app):
    if (obj.get_role_name() == 'push button' and
        obj.get_name() == 'Expandir contactos'):
        break
else:
    assert False, "No pude encontrar el botón 'Expandir contactos'"

## Busco al acción 'click' en el botón
for idx in range(obj.get_n_actions()):
    if obj.get_action_name(idx) == 'click':
        break
else:
    assert False, "El botón 'Expandir contactos' no tiene una acción 'click'"

## Lanzo la acción
obj.do_action(idx)
time.sleep(1)

# THEN Busco el botón Home
for obj in tree_walk(app):
    if (obj.get_role_name() == 'push button' and
            obj.get_name() == 'Home'):
        break
else:
    assert False, "No pude encontrar la etiqueta Home"

# Busco al acción 'click' en el botón
for idx in range(obj.get_n_actions()):
    if obj.get_action_name(idx) == 'click':
        break
else:
    assert False, "El botón 'Home' no tiene una acción 'click'"

## Lanzo la acción
obj.do_action(idx)
time.sleep(1)

# THEN pulso el botón 'Buscar'
for obj in tree_walk(app):
    if (obj.get_role_name() == 'push button' and
        obj.get_name() == 'Buscar'):
        break
else:
    assert False, "No pude encontrar el botón 'Buscar'"

process and process.kill()

#-------------------------------------------------------------------------------
# Noveno test
#-------------------------------------------------------------------------------

# GIVEN he lanzado la aplicación

## Ejecuto la aplicación en un proceso del S.O.
exit_code = subprocess.run(['bash','./stop.sh'])
path = "./ipm-p1.py"
name = f"{path}-test-{str(random.randint(0, 100000000))}"
process = subprocess.Popen([path, '--name', name])
assert process is not None, f"No pude ejecuar la aplicación {path}"

## Espero hasta que la aplicación aparezca en el escritorio
## Pasado un timeout abandono la espera
desktop = Atspi.get_desktop(0)
start = time.time()
timeout = 10
app = None
while app is None and (time.time() - start) < timeout:
    gen = filter(lambda child: child and child.get_name() == name,
                 (desktop.get_child_at_index(i) for i in range(desktop.get_child_count())))
    app = next(gen, None)
    if app is None:
        time.sleep(2)

## Compruebo que todo fue bien
if app is None:
    process and process.kill()
    assert False, f"La aplicación {path} no aparece en el escritorio"


## Cambio el nombre
for obj in tree_walk(app):
    if (obj.get_role_name() == 'text' and
        obj.get_text(0, -1) == ("")):
        obj.set_text_contents('Nieves Vargas')
        break
else:
    assert False, "No pude encontrar el Nombre'"

# WHEN pulso el botón 'Buscar'
for obj in tree_walk(app):
    if (obj.get_role_name() == 'push button' and
        obj.get_name() == 'Buscar'):
        break
else:
    assert False, "No pude encontrar el botón 'Buscar'"
## Busco al acción 'click' en el botón
for idx in range(obj.get_n_actions()):
    if obj.get_action_name(idx) == 'click':
        break
else:
    assert False, "El botón 'Buscar' no tiene una acción 'click'"    

## Lanzo la acción
obj.do_action(idx)
time.sleep(2)

## Busco el label Dialogo
for obj in tree_walk(app):
    if (obj.get_role_name() == 'label' and
        obj.get_text(0, -1).startswith("Error")):
        break
else:
    assert False, "No pude encontrar la etiqueta Dialogo'"

    ## Compruebo el contenido
assert obj.get_text(0, -1) == "Error de conexión! Por favor, reinicia la aplicación"

# WHEN pulso el botón 'Close'
## Busco el Close
for obj in tree_walk(app):
    if (obj.get_role_name() == 'push button' and
        obj.get_name() == 'Close'):
        break
else:
    assert False, "No pude encontrar el botón 'Close'"


## Busco al acción 'click' en el botón
for idx in range(obj.get_n_actions()):
    if obj.get_action_name(idx) == 'click':
        break
else:
    assert False, "El botón 'Close' no tiene una acción 'click'"    

## Lanzo la acción
obj.do_action(idx)
time.sleep(1)


process and process.kill()

