# Sistema de Líneas — Proyecto MVC en Python

Proyecto de práctica para aprender a organizar un programa con el patrón
**MVC (Modelo – Vista – Controlador)**. El programa permite **agregar, listar,
editar y eliminar** líneas, y las guarda en un archivo de texto.

Está pensado para estudiantes que **empiezan** con Python: el código es sencillo
y está muy comentado.

---

## 📑 Índice

1. [¿Qué hace el programa?](#-qué-hace-el-programa)
2. [Cómo ejecutarlo](#-cómo-ejecutarlo)
3. [Estructura de carpetas](#-estructura-de-carpetas)
4. [El patrón MVC explicado fácil](#-el-patrón-mvc-explicado-fácil)
5. [El campo `id` autoincrementable](#-el-campo-id-autoincrementable)
6. [Conceptos de Python usados](#-conceptos-de-python-usados)
7. [Manejo de errores con `try / except`](#-manejo-de-errores-con-try--except)
8. [Cómo se guardan los datos](#-cómo-se-guardan-los-datos)

---

## 🎯 ¿Qué hace el programa?

Un menú por consola con 5 opciones:

```
----- SISTEMA DE LINEAS -----
1. Agregar linea
2. Listar lineas
3. Editar linea
4. Eliminar linea
5. Salir
```

Cada línea tiene 3 datos:

| Campo    | ¿Qué es?                                   | ¿Quién lo pone?              |
|----------|--------------------------------------------|------------------------------|
| `id`     | Número único que identifica la línea       | El programa (automático)     |
| `nombre` | Texto con el nombre de la línea            | El usuario                   |
| `orden`  | Número que indica el orden                 | El usuario                   |

---

## ▶️ Cómo ejecutarlo

Desde la carpeta del proyecto:

```bash
python main.py
```

Luego elige la opción **1 (Líneas)** y sigue el menú.

Los datos se guardan solos en `media/tiendavirtual.txt`.

---

## 📂 Estructura de carpetas

```
tallers7llerena/
│
├── main.py                     # Punto de entrada: enciende el programa
│
├── modelo/
│   └── mdl_linea.py            # MODELO: define QUÉ es una Línea
│
├── controlador/
│   └── ctr_linea.py            # CONTROLADOR: guarda y lee del archivo
│
├── vista/
│   └── view_linea.py           # VISTA: menú, pedir datos y mostrar
│
└── media/
    └── tiendavirtual.txt       # "Base de datos" en texto (se crea sola)
```

> 💡 Los archivos `__init__.py` (vacíos) convierten cada carpeta en un
> **paquete** de Python, para poder hacer `from modelo.mdl_linea import Linea`.

**Convención de nombres de archivo:**
`mdl_` = modelo, `ctr_` = controlador, `view_` = vista.

---

## 🧩 El patrón MVC explicado fácil

MVC separa el programa en **3 partes**, cada una con **un solo trabajo**. Así el
código es más ordenado y fácil de mantener.

Piensa en un **restaurante**:

| Parte           | Archivo           | En el restaurante | Su único trabajo                         |
|-----------------|-------------------|-------------------|------------------------------------------|
| **Modelo**      | `mdl_linea.py`    | La receta         | Define QUÉ es una Línea y sus reglas     |
| **Vista**       | `view_linea.py`   | El mesero         | Habla con el usuario (menú, pedir, mostrar) |
| **Controlador** | `ctr_linea.py`    | La cocina         | Guarda y lee los datos del archivo       |

**Regla de oro:** cada parte NO se mete en el trabajo de la otra.
- La Vista **no** guarda archivos → le pide al Controlador.
- El Controlador **no** muestra menús → eso es de la Vista.
- El Modelo **no** pide datos ni guarda → solo describe la Línea.

### ¿Cómo se comunican? (flujo al agregar una línea)

```
Usuario  →  VISTA          →  CONTROLADOR        →  MODELO
           (pide nombre        (calcula el id,       (crea el objeto
            y orden)            guarda en archivo)     Linea)
```

1. La **Vista** pide `nombre` y `orden` por teclado.
2. Se los pasa al **Controlador**: `self.controlador.agregar(nombre, orden)`.
3. El **Controlador** pide un id nuevo al **Modelo** y crea una `Linea`.
4. El **Controlador** la guarda en el archivo.

---

## 🔢 El campo `id` autoincrementable

El `id` es un número **único** que se genera **solo**. El usuario nunca lo
escribe. Así se calcula (en el Modelo, `mdl_linea.py`):

```python
@staticmethod
def siguiente_id(lineas):
    # El id nuevo = el id mas alto que ya existe + 1.
    # Si no hay ninguna linea todavia, empieza en 1.
    mayor = 0
    for linea in lineas:
        if linea.id > mayor:
            mayor = linea.id
    return mayor + 1
```

**Ejemplo:** si ya existen los ids `1, 2, 5` → la siguiente será `6`.

Ventajas de hacerlo con "el más alto + 1":
- Nunca se repite un id, aunque **borres** líneas del medio.
- Funciona aunque **cierres y vuelvas a abrir** el programa (mira el archivo).

> El `id` es de **solo lectura**: una vez creado, no se puede cambiar (ver la
> sección de `@property` más abajo).

---

## 🐍 Conceptos de Python usados

Toda esta sección se ve en `modelo/mdl_linea.py`. Aquí la diferencia entre cada
cosa, bien básico:

### 1. La clase → `class Linea`

Un **molde** para crear objetos. `class Linea` describe cómo es cualquier línea.

### 2. El constructor → `__init__`

```python
def __init__(self, nombre, orden, id):
    self._id = int(id)
    self._nombre = nombre
    self._orden = orden
```

- Se ejecuta **automáticamente** al crear una línea: `Linea("Camisetas", "2", 1)`.
- Su trabajo: **guardar los datos iniciales** del objeto.
- `self` significa **"este objeto que estoy creando ahora"**.

### 3. `@property` → un dato "protegido"

```python
@property
def nombre(self):
    return self._nombre

@nombre.setter
def nombre(self, valor):
    self._nombre = valor
```

- Deja usar `linea.nombre` **como si fuera un atributo** (sin paréntesis).
- El dato real vive escondido en `self._nombre` (con guion bajo).
- **getter** (`@property`) = para **leer**.
- **setter** (`@nombre.setter`) = para **escribir**.

El `id` tiene getter pero **NO** setter → por eso es de **solo lectura**:

```python
linea.nombre = "Gorras"   # ✅ OK  (nombre tiene setter)
linea.id = 99             # ❌ ERROR (id no tiene setter)
```

### 4. `@staticmethod` → un método que NO usa `self`

```python
@staticmethod
def siguiente_id(lineas):
    ...
```

- **No** necesita un objeto concreto (por eso **no lleva `self`**).
- Se llama con el **nombre de la clase**: `Linea.siguiente_id(lista)`.
- Ideal para `siguiente_id`, porque la línea nueva **todavía no existe**.

### Tabla resumen

| Concepto        | ¿Lleva `self`? | ¿Cómo se usa?              | ¿Para qué sirve?                       |
|-----------------|:--------------:|----------------------------|----------------------------------------|
| `__init__`      | Sí             | `Linea(...)`               | Armar el objeto con sus datos          |
| Método normal   | Sí             | `linea.metodo()`           | Trabajar con **una** línea concreta    |
| `@property`     | Sí             | `linea.nombre` (sin `()`)  | Leer/escribir un dato **controlado**   |
| `@staticmethod` | **No**         | `Linea.siguiente_id(...)`  | Tarea de la clase, sin un objeto       |

**Idea clave:** `self` = "un objeto concreto".
Si el método necesita un objeto → lleva `self`. Si no → es `@staticmethod`.

---

## 🛡️ Manejo de errores con `try / except`

En la **Vista**, las operaciones de agregar, editar y eliminar están protegidas:

```python
try:
    self.controlador.eliminar(id)
    print("\nLinea eliminada.")
except Exception as ex:
    print(f"\nNo se pudo eliminar la linea: {ex}")
```

- Si algo falla (por ejemplo, el **id no existe**), el programa **no se cae**.
- Muestra un mensaje claro y el menú **sigue funcionando**.

El error del id inexistente nace en el **Controlador**:

```python
raise ValueError(f"No existe una linea con id {id}")
```

...y lo **atrapa** el `try / except` de la Vista. Así el Controlador avisa del
problema y la Vista decide cómo mostrárselo al usuario.

---

## 💾 Cómo se guardan los datos

Todo se guarda en `media/tiendavirtual.txt`, una línea de texto por registro,
con los datos separados por comas:

```
id,nombre,orden
```

Ejemplo del contenido del archivo:

```
1,Camisetas,2
2,Pantalones,1
3,Zapatos,3
```

- Al **guardar**, el Controlador escribe TODA la lista (borra lo viejo y pone lo nuevo).
- Al **leer**, el Controlador parte cada línea por las comas con `l.split(",")`
  y crea un objeto `Linea` por cada fila.
- La carpeta `media/` y el archivo se crean **solos** la primera vez.

---

## ✅ Resumen para recordar

- **MVC** = separar en 3 partes con un solo trabajo cada una.
- **Modelo** describe, **Vista** habla con el usuario, **Controlador** guarda/lee.
- El **`id`** se genera solo (`el más alto + 1`) y es de solo lectura.
- **`@property`** protege los datos; **`@staticmethod`** no necesita un objeto.
- **`try / except`** evita que el programa se caiga y muestra errores claros.
