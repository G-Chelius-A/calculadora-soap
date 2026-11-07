# ACTIVIDADES - UNIDAD 4 (SOAP) - SOA
----
Por: Gerardo Yeray Chelius Altamirano | 7°B Ingeniería en Sistemas Computacionales | UCC | 2026
---

### Instrucciones de instalación y ejecución
1. Instalar Python 3.10.
2. Desde la carpeta del proyecto, crear el entorno virtual (si todavía no existe):
   ```powershell
   python -m venv venv
   ```
3. Activar el entorno virtual en Windows PowerShell:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   En el símbolo del sistema (CMD), usar:
   ```bat
   .\venv\Scripts\activate.bat
   ```
4. Instalar las dependencias:
   ```powershell
   python -m pip install zeep spyne lxml
   ```
5. Iniciar el servidor de la actividad en una terminal:
   ```powershell
   python Server.py
   ```
   En otra terminal, activar el entorno virtual y ejecutar el cliente correspondiente. Para detener un servidor, presionar `Ctrl+C`.

Cada actividad utiliza un puerto distinto: calculadora `8000`, biblioteca `8001` y tienda `8002`. El cliente se conecta al WSDL local de su servidor, por lo que primero debe iniciarse el servidor.

---
## Actividad 0: Creación de un servicio web WSDL con Python
Se implementa una calculadora SOAP con Spyne como servidor y Zeep como cliente. El servicio ofrece las operaciones:

| Operación | Entradas (tipo Spyne) | Salida (tipo Spyne) |
|---|---|---|
| `sumar` | `a: Integer`, `b: Integer` | `Integer` |
| `restar` | `a: Integer`, `b: Integer` | `Integer` |
| `dividir` | `a: Integer`, `b: Integer` | `Integer` (división entera) |
| `multiplicar` | `a: Integer`, `b: Integer` | `Integer` |

El servidor publica el WSDL en `http://127.0.0.1:8000/?wsdl`. En una terminal:
```powershell
python Server.py
```
En otra terminal:
```powershell
python Cliente.py
```
El cliente prueba las cuatro operaciones y muestra el error cuando se intenta dividir entre cero.

---
## Actividad 1: Consulta de una biblioteca
El servidor consulta un catálogo de libros definido en memoria. Las operaciones SOAP son:

| Operación | Entrada (tipo Spyne) | Salida (tipo Spyne) |
|---|---|---|
| `buscar_titulo` | `code: Unicode` | `Unicode` |
| `ejemplares_disponibles` | `code: Unicode` | `Integer` |
| `hay_disponibilidad` | `code: Unicode` | `Boolean` |
| `mostrar_todos` | Sin entrada | `Unicode` |

Si el código consultado no existe, las tres operaciones de consulta por código devuelven un error SOAP. El WSDL está en `http://127.0.0.1:8001/?wsdl`.

En una terminal:
```powershell
python ServerLibrary.py
```
En otra terminal:
```powershell
python ClientLibrary.py
```
El cliente prueba consultas existentes e inexistentes y solicita el catálogo completo.

---
## Actividad 2: Servicio web de una tienda
El servicio procesa pedidos utilizando un inventario en memoria. Cada pedido incluye un cliente y una o más líneas con el código de producto y la cantidad. El servidor comprueba que los productos existan y que haya suficiente stock; al registrar el pedido, calcula el total y descuenta las unidades del inventario.

| Operación | Entrada (tipo Spyne) | Salida (tipo Spyne) |
|---|---|---|
| `registrar_pedido` | `Pedido` (`ComplexModel`): `cliente: String`, `linea: Array(LineaPedido)`; `LineaPedido` (`ComplexModel`): `producto: String`, `cantidad: Integer` | `Confirmacion` (`ComplexModel`): `pedido_id: Integer`, `cliente: String`, `total: Float` |
| `consultar_pedido` | `pedido_id: Integer` | `Confirmacion` y `Pedido` (`ComplexModel`) |

El WSDL está en `http://127.0.0.1:8002/?wsdl`.

En una terminal:
```powershell
python ServerTienda.py
```
En otra terminal:
```powershell
python ClientTienda.py
```
El cliente prueba pedidos válidos, falta de stock, productos y pedidos inexistentes, además de entradas incompletas.

---
## Estructura de carpetas y archivos
```text
calculadora-soap/
├── Cliente.py
├── ClientLibrary.py
├── ClientTienda.py
├── Server.py
├── ServerLibrary.py
├── ServerTienda.py
├── README.md
└── venv/
    ├── Include/
    ├── Lib/
    │   └── site-packages/
    ├── Scripts/
    └── pyvenv.cfg
```

### Archivos Python del proyecto
- `Server.py`: servidor SOAP de la calculadora; publica las operaciones aritméticas en el puerto `8000`.
- `Cliente.py`: cliente Zeep de la calculadora; invoca las operaciones del servidor.
- `ServerLibrary.py`: servidor SOAP de la biblioteca; contiene el catálogo y publica consultas en el puerto `8001`.
- `ClientLibrary.py`: cliente Zeep de la biblioteca; consulta libros, disponibilidad y catálogo.
- `ServerTienda.py`: servidor SOAP de la tienda; gestiona inventario, registro y consulta de pedidos en el puerto `8002`.
- `ClientTienda.py`: cliente Zeep de la tienda; envía pedidos y prueba distintos casos de consulta y validación.

### Carpetas y configuración de `venv`
- `Include/`: contiene encabezados de C que pueden ser necesarios para compilar algunas extensiones de Python.
- `Lib/`: contiene las bibliotecas instaladas en el entorno virtual. `Lib/site-packages/` es donde se encuentran paquetes como Spyne, Zeep y sus dependencias.
- `Scripts/`: contiene el ejecutable de Python y herramientas del entorno, además de los scripts para activarlo (`Activate.ps1` y `activate.bat`).
- `pyvenv.cfg`: archivo de configuración del entorno virtual; indica el intérprete base y su versión, entre otros ajustes.

`venv` es un entorno local generado para este proyecto; no contiene el código de las actividades. Si se elimina, puede volver a crearse siguiendo las instrucciones de instalación.
