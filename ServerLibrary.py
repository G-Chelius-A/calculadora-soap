from spyne import Application, rpc, ServiceBase, Integer, Unicode, Boolean
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.model.fault import Fault

from wsgiref.simple_server import make_server

CATALOG = {
        "LIB-001": {"titulo": "Cien años de soledad", "numero_ejemplares": 5, "disponible": True},
        "LIB-002": {"titulo": "La vorágine", "numero_ejemplares": 0, "disponible": False},
        "LIB-999": {"titulo": "No encontrado", "numero_ejemplares": 0, "disponible": False}
    }

class LibraryService(ServiceBase):


    @rpc(Unicode, _returns=Unicode)
    def buscar_titulo(ctx, code):
        libro = CATALOG.get(code)

        if libro is None:
            raise Fault(faultcode="Client.LibroNoEncontrado", faultstring="Libro no encontrado")

        return libro["titulo"]


    @rpc(Unicode, _returns=Integer)
    def ejemplares_disponibles(ctx, code):
        libro = CATALOG.get(code)

        if libro is None:
            raise Fault(faultcode="Client.LibroNoEncontrado", faultstring="Libro no encontrado")

        return libro["numero_ejemplares"]


    @rpc(Unicode, _returns=Boolean)
    def hay_disponibilidad(ctx, code):
        libro = CATALOG.get(code)

        if libro is None:
            raise Fault(faultcode="Client.LibroNoEncontrado", faultstring="Libro no encontrado")

        return libro["disponible"]

    # Método para mostrar todos los libros en el catálogo | No solicitado en la actividad, pero útil para pruebas.
    @rpc(_returns=Unicode)
    def mostrar_todos(ctx):

        cadenaLibros = "Catálogo completo: \n"

        for codigo, libro in CATALOG.items():
            cadenaLibros += f"Código: {codigo}, Título: {libro['titulo']}, Ejemplares: {libro['numero_ejemplares']}, Disponible: {libro['disponible']}\n"
        return cadenaLibros


application = Application([LibraryService], 'spyne.library.soap',
                          in_protocol=Soap11(validator="lxml"),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
    server = make_server('0.0.0.0', 8000, wsgi_application)
    print("El servidor SOAP está escuchando en: http://127.0.0.1:8000")
    print("WSDL ejecutándose en: http://127.0.0.1:8000/?wsdl")
    server.serve_forever() # Mantiene el servidor en ejecución