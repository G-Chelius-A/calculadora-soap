from zeep import Client
from zeep.exceptions import Fault

wsdl_url = 'http://127.0.0.1:8000/?wsdl'

try:
    cliente = Client(wsdl=wsdl_url)
    print("Cliente conectado al WSDL:", wsdl_url)
    
    busca_titulo = cliente.service.buscar_titulo("LIB-001")
    print("Título encontrado:", busca_titulo)

    ejemplares_disponibles = cliente.service.ejemplares_disponibles("LIB-002")
    print("Ejemplares disponibles:", ejemplares_disponibles)

    hay_disponibilidad = cliente.service.hay_disponibilidad("LIB-999")
    print("¿Está disponible el libro?", hay_disponibilidad)

    # Buscar un libro inexistente
    try:
        libro_inexistente = cliente.service.buscar_titulo("LIB-666")
        print("Título encontrado:", libro_inexistente)
    except Fault as e:
        print("Error al buscar libro inexistente:", e)

    # Consultar ejemplares de un libro inexistente
    try:
        ejemplares_inexistentes = cliente.service.ejemplares_disponibles("LIB-666")
        print("Ejemplares disponibles:", ejemplares_inexistentes)
    except Fault as e:
        print("Error al consultar ejemplares de libro inexistente:", e)

    # Consultar disponibilidad de un libro inexistente
    try:
        disponibilidad_inexistente = cliente.service.hay_disponibilidad("LIB-666")
        print("¿Está disponible el libro?", disponibilidad_inexistente)
    except Fault as e:
        print("Error al consultar disponibilidad de libro inexistente:", e)

    # Consultar todos los libros en el catálogo
    todos_los_libros = cliente.service.mostrar_todos()
    print(todos_los_libros)

except Exception as e:
    print("Error al conectar al servidor WSDL:", e)