# Guion para explicar el modulo de MARCA paso a paso

> Objetivo: que cualquiera entienda como funciona el CRUD de Marca con el
> patron MVC (Modelo - Vista - Controlador), aunque nunca lo haya visto.

---

## 1. Empezar con la idea general (2 min)

Decir algo asi:

> "Vamos a hacer un catalogo de Marcas para una tienda. Una marca es algo
> muy simple: tiene un **id** (su numero unico) y un **nombre** (ej: Nike).
> Queremos poder **agregarlas,
> listarlas, editarlas y eliminarlas**: eso se llama un CRUD."

Luego explicar por que dividimos el codigo en 3 archivos (MVC):

| Archivo | Rol | Pregunta que responde |
|---|---|---|
| `modelo/mdl_marca.py` | MODELO | ¿**QUE** es una marca? |
| `controlador/ctr_marca.py` | CONTROLADOR | ¿**DONDE y COMO** se guarda? |
| `vista/view_marca.py` | VISTA | ¿**COMO** interactua el usuario? |

Analogia util: un restaurante.
- La **Vista** es el mesero: habla con el cliente, toma el pedido.
- El **Controlador** es la cocina: prepara y guarda las cosas.
- El **Modelo** es la receta: define que lleva cada plato.

El mesero no cocina y la cocina no habla con el cliente. Igual aqui:
la Vista nunca escribe en el archivo y el Controlador nunca hace `input()`.

---

## 2. El MODELO: `modelo/mdl_marca.py` (5 min)

**Paso 1 — La clase y el constructor.**

```python
class Marca:
    def __init__(self, nombre, id):
        self._id = int(id)
        self._nombre = nombre
```

> "El constructor solo GUARDA los 2 datos. No valida, no pregunta nada.
> El guion bajo (`_id`) es una convencion de Python que significa:
> 'este dato es interno, no lo toques directo desde fuera'."

**Paso 2 — El id autoincrementable.**

```python
@staticmethod
def siguiente_id(marcas):
    mayor = 0
    for marca in marcas:
        if marca.id > mayor:
            mayor = marca.id
    return mayor + 1
```

> "El usuario NUNCA escribe el id: se calcula solo. La regla es: busco el
> id mas grande que ya existe y le sumo 1. Si hay ids 1, 2 y 5, el nuevo
> sera 6. Si no hay ninguna marca, empieza en 1."
>
> "Es `@staticmethod` porque no necesita una marca concreta (no usa
> `self`): solo mira la lista completa."

**Paso 3 — Las properties.**

```python
@property
def id(self):
    return self._id

@property
def nombre(self):
    return self._nombre

@nombre.setter
def nombre(self, valor):
    self._nombre = valor
```

> "Una property permite leer el dato como si fuera una variable normal:
> `marca.nombre`, sin parentesis. `@property` es la funcion para LEER y
> `@nombre.setter` es la funcion para CAMBIAR. Fijense que `id` NO tiene
> setter: por eso el id no se puede cambiar desde fuera. `nombre` si lo
> tiene porque ese si se puede editar."

---

## 2.1 Como explicar `@property` a fondo (5 min)

**Paso 1 — Empezar por el problema (sin property).**

> "Cuando creamos una marca, sus datos quedan guardados con guion bajo:
> `_nombre`, `_id`. Ese guion bajo es una señal en Python que significa:
> 'esto es interno, no lo toques directo'. Pero si alguien escribe
> `marca._id = 999`, Python lo deja... y nos rompe todo el sistema,
> porque el id debe ser unico."

**Paso 2 — La solucion: la analogia de la ventanilla.**

> "Por eso abrimos ventanillas de atencion: los datos quedan guardados
> en bodega (los `_algo`) y las properties son las ventanillas por donde
> se piden. Tu decides que ventanillas abrir."

```python
@property
def nombre(self):          # ventanilla para LEER
    return self._nombre

@nombre.setter
def nombre(self, valor):   # ventanilla para ESCRIBIR
    self._nombre = valor
```

**Paso 3 — El detalle que sorprende: se usa SIN parentesis.**

> "Aunque es un metodo, se usa como si fuera una variable: escribes
> `marca.nombre`, no `marca.nombre()`. Python ve el `@property` y
> ejecuta el metodo por ti: si LEO `marca.nombre` llama a la funcion de
> arriba, y si ASIGNO `marca.nombre = 'Nike'` llama a la del setter.
> Por fuera parece un dato simple; por dentro hay un metodo
> controlandolo."

**Paso 4 — El remate: el id NO tiene setter.**

> "Miren el `id`: tiene ventanilla para leer pero NO tiene `@id.setter`.
> O sea: abrimos la ventanilla de lectura y la de escritura la dejamos
> cerrada. Por eso el id no se puede cambiar desde fuera, ni por error."

**Demo en vivo (30 segundos, en la consola de Python):**

```python
>>> from modelo.mdl_marca import Marca
>>> m = Marca("Nike", 1)
>>> m.nombre              # lee: 'Nike' (sin parentesis)
>>> m.nombre = "Adidas"   # escribe: por dentro llama al setter
>>> m.id = 99             # ERROR: AttributeError, no tiene setter
```

Ese `AttributeError` en vivo es el momento "aja": la property protege el dato.

---

## 2.2 Como explicar `@staticmethod` a fondo (5 min)

**Paso 1 — Empezar por lo normal.**

> "Un metodo normal siempre recibe `self`, que significa 'ESTA marca en
> concreto'. Por ejemplo, `m.nombre` es el nombre de ESA marca. Para
> usarlo necesitas tener una marca en la mano."

**Paso 2 — El problema que lo justifica (el argumento clave).**

> "Ahora piensen en `siguiente_id`. Sirve para calcular el id de una
> marca **que todavia no existe**. ¿Como le voy a preguntar su id a una
> marca que aun no he creado? No puedo. Es el huevo y la gallina:
> necesito el id ANTES de crear el objeto."

**Paso 3 — La solucion.**

> "Por eso es `@staticmethod`: es una funcion que NO usa `self` — no le
> importa ninguna marca en concreto, solo mira la lista completa y
> devuelve el mayor + 1. La ponemos DENTRO de la clase solo porque el
> tema es 'cosas de marcas', para tenerla ordenada ahi."

Analogia:

> "Es como una calculadora colgada en la pared de la bodega: pertenece a
> la bodega porque ahi se usa, pero no pertenece a ninguna caja en
> particular."

**Paso 4 — Como se llama: con el nombre de la CLASE, no de un objeto.**

```python
nuevo_id = Marca.siguiente_id(marcas)   # con la clase, sin crear ninguna marca
```

> "Fijense: `Marca.siguiente_id(...)`, no `m.siguiente_id(...)`. No
> necesite ningun objeto. Asi lo usa el controlador en `agregar()`:
> primero calcula el id con el static method, y CON ese id ya crea la
> marca."

**La comparacion final (dejarla en la pizarra):**

| | Metodo normal / property | `@staticmethod` |
|---|---|---|
| ¿Recibe `self`? | Si ("esta marca") | No |
| ¿Necesita un objeto creado? | Si | No |
| ¿Como se llama? | `m.nombre` | `Marca.siguiente_id(lista)` |
| Ejemplo en el proyecto | leer/cambiar el nombre | calcular el id del siguiente |

**Pregunta trampa que pueden hacer:** *"¿Por que no calcular el id
dentro del constructor?"* → Porque el constructor debe ser tonto: solo
guardar lo que le den. Si calculara el id, al LEER el archivo se
recalcularian los ids y se perderian los originales. Por eso el id se
calcula fuera (con el static method) y el constructor solo lo recibe.

---

## 3. El CONTROLADOR: `controlador/ctr_marca.py` (7 min)

**Paso 1 — Como se guardan los datos.**

> "Usamos un archivo de texto `media/marcas.txt`. Cada marca es una fila
> separada por comas, como una mini base de datos:"

```
1,Nike
2,Adidas
```

**Paso 2 — El constructor prepara la ruta.**

```python
raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
carpeta = os.path.join(raiz, "media")
os.makedirs(carpeta, exist_ok=True)
self.archivo = os.path.join(carpeta, "marcas.txt")
```

> "Esto solo calcula donde esta la carpeta `media` del proyecto y crea la
> carpeta si no existe, para que nunca falle por eso."

**Paso 3 — `listar()`: de texto a objetos.**

```python
id, nombre = l.split(",")
marca = Marca(nombre, id)
```

> "Leemos el archivo fila por fila. `split(',')` corta la fila en 3
> pedazos y con ellos construimos un objeto `Marca`. Ojo: pasamos el id
> que YA estaba guardado, para conservarlo. Si el archivo no existe
> todavia, el `except FileNotFoundError` devuelve la lista vacia."

**Paso 4 — `guardar()`: de objetos a texto.**

> "Es el proceso inverso: recorre la lista y escribe cada marca como una
> fila. Usa modo `'w'`: borra todo y escribe la lista completa de nuevo."

**Paso 5 — `agregar()`, el flujo completo.**

```python
def agregar(self, nombre):
    marcas = self.listar()                  # 1. leo lo que hay
    nuevo_id = Marca.siguiente_id(marcas)   # 2. calculo el id nuevo
    marcas.append(Marca(nombre, nuevo_id))          # 3. agrego a la lista
    self.guardar(marcas)                    # 4. guardo todo
```

> "Siempre el mismo patron: leer → modificar la lista → guardar."

**Paso 6 — `editar()` y `eliminar()`: buscar POR ID.**

> "Recorremos la lista comparando `marcas[i].id == id`. Buscamos por ID,
> no por posicion, porque si borras la marca 2, la que era tercera pasa a
> segunda posicion, pero su id no cambia. Si el bucle termina sin
> encontrar el id, lanzamos `raise ValueError(...)`: ese error viaja
> hasta la Vista, que lo atrapa y muestra el mensaje sin que el programa
> se caiga."

---

## 4. La VISTA: `vista/view_marca.py` (5 min)

**Paso 1 — El menu (`iniciar`).**

> "Un `while True` que muestra las 5 opciones y llama al metodo que
> corresponda. Solo se rompe (`break`) con la opcion 5."

**Paso 2 — Las validaciones ANTES de llamar al controlador.**

```python
nombre = input("Nombre: ").strip()
if nombre == "":
    print("Nombre no puede estar vacio.")
    return
```

> "La Vista es el filtro: si el dato esta mal, ni siquiera molestamos al
> controlador."

**Paso 3 — El try/except.**

```python
try:
    self.controlador.agregar(nombre)
    print("\nMarca agregada.")
except Exception as ex:
    print(f"\nNo se pudo agregar la marca: {ex}")
```

> "Si algo falla (el id no existe, no se puede escribir el archivo), el
> programa NO se cae: mostramos el error y el menu sigue funcionando."

**Paso 4 — Numero de pantalla vs id.**

> "Al listar salen dos numeros: `1). (id: 3) Nike`. El primero es solo la
> posicion en pantalla; el que esta entre parentesis es el id real, y ese
> es el que se pide para editar o eliminar."

---

## 5. Demo en vivo (3 min)

1. Ejecutar `python main.py` → opcion `1` (Marcas).
2. Agregar "Nike" y "Adidas". Listar: ids 1 y 2.
3. Abrir `media/marcas.txt` y mostrar las filas → "esto es todo lo que hay detras".
4. Eliminar la marca 1 y agregar otra → el id nuevo es 3, no 1: los ids no se reciclan.
5. Intentar editar el id 99 → muestra el error y el programa sigue vivo.

---

## 6. Preguntas tipicas y sus respuestas

- **¿Por que 3 archivos y no 1?** → Para que cada parte tenga UNA
  responsabilidad. Si mañana cambiamos el archivo de texto por una base
  de datos real, solo tocamos el Controlador; la Vista y el Modelo no se
  enteran.
- **¿Por que el id no tiene setter?** → Porque el id es la identidad del
  registro: si se pudiera cambiar, podrias duplicarlo o romper referencias.
- **¿Que pasa si dos marcas se llaman igual?** → El sistema las acepta
  porque lo que las distingue es el id (mejora posible: validar duplicados).
