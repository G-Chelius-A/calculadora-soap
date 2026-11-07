from spyne import Application, rpc, ServiceBase, Integer
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

from wsgiref.simple_server import make_server

# Clase CalculadoraService que hereda de ServiceBase, como clase Base.
class CalculadoraService(ServiceBase):


    # ctx y rpc son decoradores, que serán invocados a partir de su nombre. Retornarán otros elementos.
    @rpc(Integer, Integer, _returns=Integer)
    def sumar(ctx, a, b):
        return a + b


    @rpc(Integer, Integer, _returns=Integer)
    def restar(ctx, a, b):
        return a - b


    @rpc(Integer, Integer, _returns=Integer)
    def dividir(ctx, a, b):
        if b == 0:
            raise ValueError("No se puede dividir entre cero.") #Excepción custom para evitar la división entre cero.
        return a // b # Para que retorne la parte entera.


    @rpc(Integer, Integer, _returns=Integer)
    def multiplicar(ctx, a, b):
        return a * b

application = Application([CalculadoraService], 'spyne.calculadora.soap',
                          in_protocol=Soap11(validator="lxml"),
                          out_protocol=Soap11()) #Se indica que se trabajará con SOAP v.1.1, hoy deprecado pero aún funcional.

wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
    server = make_server('0.0.0.0', 8000, wsgi_application) #Especifica la dirección IP, el puerto y la aplicación SOAP.
    print("Servidor SOAP escuchando en http://127.0.0.1:8000")
    print("El WSDL está ejecutándose en http://127.0.0.1:8000/?wsdl")
    server.serve_forever() # Mantiene el servidor en ejecución