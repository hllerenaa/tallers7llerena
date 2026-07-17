# Guion para explicar el modulo de PRODUCTO (articulo) paso a paso

> Objetivo: que se entienda lo NUEVO de este modulo: las **claves foraneas
> (FK)**. Marca, Categoria y Linea son catalogos sueltos; el Producto es
> quien los conecta. Conviene explicar este modulo DESPUES del de Marca.
>
> Apoyo visual: la pagina de diagramas (el UML muestra las FK con flechas
> y el diagrama de flujo 4 es exactamente "agregar producto"):
> https://claude.ai/code/artifact/423f185b-9e39-4887-ab48-27f41678460b

---

## 1. La idea clave: el Producto relaciona los catalogos (3 min)

Empezar dibujando esto en la pizarra:

```
MARCA                 CATEGORIA              LINEA
id | nombre           id | nombre            id | nombre
1  | Nike             1  | Calzado           1  | Deportiva
2  | Adidas           2  | Ropa              2  | Casual

                 PRODUCTO
id | nombre        | id_marca | id_categoria | id_linea | precio | stock
1  | Zapatilla Air |    1     |      1       |    1     | 59.99  |  10
```

Decir:

> "El producto NO guarda el texto 'Nike'. Guarda el **numero 1**, que es
> el id de Nike en el catalogo de marcas. Ese numero se llama **clave
> foranea (FK)**: una llave que apunta a un registro de OTRA tabla."

¿Por que guardar el numero y no el nombre?

> "Si mañana la marca cambia de nombre, se corrige UNA vez en su catalogo
> y todos los productos quedan actualizados automaticamente, porque ellos
> solo guardan el id. Ademas evita errores de escritura: no puede existir
> un producto 'Nkie' con falta de ortografia."

Y el punto del diseño que pide el ejercicio:

> "Fijense que la **Linea es independiente de la Categoria**: la linea
> 'Deportiva' no pertenece a 'Calzado' ni a 'Ropa'. Puede haber calzado
> deportivo y ropa deportiva. Quien combina categoria y linea es cada
> producto, no los catalogos entre si."

---

## 2. El MODELO: `modelo/mdl_producto.py` (4 min)

**Paso 1 — El constructor con 7 campos.**

```python
def __init__(self, nombre, id_marca, id_categoria, id_linea, precio, stock, id):
    self._id = int(id)
    self._nombre = nombre
    self._id_marca = int(id_marca)
    self._id_categoria = int(id_categoria)
    self._id_linea = int(id_linea)
    self._precio = float(precio)
    self._stock = int(stock)
```

Puntos a remarcar:

> "Cada dato se convierte a su tipo correcto: las FK y el stock a `int`,
> el precio a `float`. Esto importa porque del archivo de texto TODO
> llega como texto, y '1' (texto) no es igual a 1 (numero)."

> "El modelo guarda las FK como numeros y ya. NO comprueba que la marca 1
> exista: eso no es su trabajo. El modelo solo define QUE es un producto."

**Paso 2 — Lo demas es identico a Marca.**

> "`siguiente_id` es el mismo de siempre (el mayor + 1) y las properties
> son iguales; el id sigue sin setter. Cuando entiendes un modelo,
> entiendes todos: solo cambian los campos."

---

## 3. El CONTROLADOR: `controlador/ctr_producto.py` (4 min)

**Paso 1 — La fila ahora tiene 7 columnas.**

```
1,Zapatilla Air,1,1,1,59.99,10
```

> "Mismo formato de siempre, pero con mas columnas. El orden es sagrado:
> se guarda y se lee EXACTAMENTE en el mismo orden."

**Paso 2 — Leer y escribir.**

```python
id, nombre, id_marca, id_categoria, id_linea, precio, stock = l.split(",")
```

> "El `split(',')` ahora reparte en 7 variables. Y `guardar()` escribe
> las 7 separadas por comas. Todo lo demas (listar → modificar →
> guardar, buscar por id, `raise ValueError` si no existe) es identico
> al controlador de Marca."

Pregunta para la clase: *"¿Que pasaria si el nombre del producto tuviera
una coma, como 'Zapatilla, roja'?"* → El `split` daria mas de 7 pedazos y
se romperia la lectura. Por eso los sistemas reales usan bases de datos o
formatos como CSV con comillas. Buena mejora a futuro.

---

## 4. La VISTA: `vista/view_producto.py` — lo mas nuevo (7 min)

**Paso 1 — Esta vista usa CUATRO controladores.**

```python
self.controlador = Controlador()              # productos
self.ctr_marca = ControladorMarca()           # para validar la FK de marca
self.ctr_categoria = ControladorCategoria()   # para validar la FK de categoria
self.ctr_linea = ControladorLinea()           # para validar la FK de linea
```

> "Para crear un producto necesito ver que marcas, categorias y lineas
> existen. Por eso la vista de productos le pide ayuda a los otros tres
> controladores."

**Paso 2 — `pedir_fk()`: el corazon del modulo.**

```python
def pedir_fk(self, lista, titulo):
    if len(lista) == 0:
        print(f"No hay {titulo} registradas...")
        return None
    # muestra el catalogo con sus ids
    # pide el id y comprueba que EXISTA en la lista
```

Explicarlo en 3 reglas:

> "Uno: si el catalogo esta vacio, no te deja continuar — no puedes crear
> un producto de una marca que no existe. Dos: te muestra las opciones
> con su id para que no adivines. Tres: comprueba que el id que
> escribiste este de verdad en la lista. Esto se llama **integridad
> referencial**: nunca guardamos una FK que apunte a la nada."

**Paso 3 — `pedir_datos()`: no repetir codigo.**

> "Agregar y editar piden exactamente los mismos 6 datos. En vez de
> copiar y pegar todo dos veces, lo pusimos en un solo metodo que usan
> ambos. Si un dato falla, devuelve `None` y no se guarda nada."

Validaciones nuevas respecto a Marca:

- Precio: `float(precio)` dentro de un try → acepta decimales (59.99) y
  rechaza texto o negativos.
- Stock: `isdigit()` → solo enteros positivos.

**Paso 4 — `mostrar()`: traducir ids a nombres.**

```python
marca = self.nombre_por_id(marcas, p.id_marca)
```

> "En el archivo esta guardado `1,1,1`, pero mostrar eso no ayuda a
> nadie. Al listar, buscamos el nombre que corresponde a cada id y
> mostramos 'Marca: Nike | Categoria: Calzado | Linea: Deportiva'. Los
> numeros se guardan; los nombres se muestran."

---

## 5. Demo en vivo (5 min)

Ya hay 4 datos de prueba en cada catalogo (marcas: Nike, Adidas, Samsung,
HP; categorias: Calzado, Ropa, Tecnologia, Hogar; lineas: Deportiva,
Casual, Premium, Economica) y 4 productos creados con ellos.

Seguir este orden (es importante):

1. Listar productos → se ven los NOMBRES: "Zapatilla Air | Marca: Nike |
   Categoria: Calzado | Linea: Deportiva".
2. Abrir `media/productos.txt` → se ven los NUMEROS: `1,Zapatilla Air,1,1,1,59.99,10`.
   Este contraste (paso 1 vs paso 2) es el momento "ajá" de las FK.
3. Agregar un producto nuevo (ej: "Mouse Gamer"): el sistema muestra cada
   catalogo y pide el id. Elegir marca 4 (HP), categoria 3 (Tecnologia),
   linea 4 (Economica), precio 15.99, stock 30.
4. Intentar poner id de marca 99 → "No existe ese id en marcas".
5. Editar la marca "Nike" a "Nike Inc" y volver a listar productos → el
   producto muestra "Nike Inc" sin haberlo tocado. **Esa es la gracia de
   guardar el id y no el nombre.**
6. Senalar los productos 3 y 4: "Televisor 50" y "Laptop Basica"
   comparten la categoria Tecnologia pero tienen lineas distintas
   (Premium y Economica) → **prueba en vivo de que la Linea es
   independiente de la Categoria.**
7. (Opcional) Borrar los archivos de `media/` y mostrar que con los
   catalogos vacios el sistema dice "No hay marcas registradas" y no
   deja crear productos: primero los catalogos, luego el producto.

---

## 6. Preguntas tipicas y sus respuestas

- **¿Por que la Linea no depende de la Categoria?** → Porque una linea
  (Deportiva, Casual, Premium) aplica a varias categorias a la vez. Si la
  linea "perteneciera" a una categoria, habria que duplicarla en cada una.
  Al ser catalogos independientes, cada producto elige libremente su
  combinacion.
- **¿Que pasa si elimino una marca que tiene productos?** → En este
  sistema el producto queda con una FK "huerfana" y al listar aparece
  "(id X no existe)". Una mejora seria impedir eliminar catalogos en uso
  (como hacen las bases de datos reales con `ON DELETE RESTRICT`).
- **¿Por que el precio es float y el stock int?** → El precio puede tener
  centavos (59.99); el stock cuenta unidades enteras, no puede haber
  media zapatilla.
