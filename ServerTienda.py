from spyne import Application, rpc, ServiceBase, Integer, String, Float, ComplexModel, Array
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.model.fault import Fault


from wsgiref.simple_server import make_server

STORE = {
        "P001": {"precio": 25.00, "stock": 10},
        "P002": {"precio": 15.00, "stock": 5}
    }

PEDIDOS = {}
CONFIRMACIONES = {}

class LineaPedido(ComplexModel):
    producto = String
    cantidad = Integer

class Pedido(ComplexModel):
    cliente = String
    linea = Array(LineaPedido, wrapped=False) # wrapped=False permite que Zeep envíe la lista de diccionarios

class Confirmacion(ComplexModel):
    pedido_id = Integer
    cliente = String
    total = Float

class StoreService(ServiceBase):

    @rpc(Pedido, _returns=Confirmacion)
    def registrar_pedido(ctx, pedido):
        total = 0.0

        if pedido.linea is None or len(pedido.linea) == 0:
            raise Exception("Error interno: no hay productos en el pedido")

        if not pedido.cliente or pedido.cliente.strip() == "":
            raise Exception("Error interno: no se ha indicado cliente.")

        # Agrupa líneas repetidas para validar la cantidad total solicitada de cada producto.
        cantidades_por_producto = {}
        for linea in pedido.linea:
            if linea.cantidad <= 0:
                raise Fault(faultcode="Client.CantidadInvalida", faultstring="La cantidad debe ser mayor que cero")

            if linea.producto not in STORE:
                raise Fault(faultcode="Client.ProductoInexistente", faultstring="Producto inexistente")

            cantidades_por_producto[linea.producto] = (
                cantidades_por_producto.get(linea.producto, 0) + linea.cantidad
            )

        for producto, cantidad in cantidades_por_producto.items():
            if cantidad > STORE[producto]["stock"]:
                raise Fault(faultcode="Client.StockInsuficiente", faultstring="Stock insuficiente")

        # Solo descuenta inventario después de comprobar el stock de todos los productos.
        for producto, cantidad in cantidades_por_producto.items():
            producto_elegido = STORE[producto]
            total += producto_elegido["precio"] * cantidad
            producto_elegido["stock"] -= cantidad

        # Clave sustituta. Se pudiese generar una clave tipo PED-0001 siguiendo f"PED-{pedido_identity:03d}" pero no es solicitado por la act.
        pedido_identity = len(PEDIDOS) + 1
        # Guarda el pedido.
        PEDIDOS[pedido_identity] = pedido

        nueva_confirmacion = Confirmacion(pedido_id=pedido_identity, cliente=pedido.cliente, total=total)
        CONFIRMACIONES[pedido_identity] = nueva_confirmacion

        # Devolver el objeto tipado de Spyne.
        return nueva_confirmacion

    @rpc(Integer, _returns=(Confirmacion, Pedido))
    def consultar_pedido(ctx, pedido_id):
        if pedido_id not in PEDIDOS:
            raise Fault(faultcode="Client.PedidoInexistente", faultstring="Pedido inexistente")

        if pedido_id not in CONFIRMACIONES:
            raise Fault(faultcode="Client.PedidoInexistente", faultstring="Pedido inexistente")

        pedido = PEDIDOS[pedido_id]

        confirmacion = CONFIRMACIONES[pedido_id]
        
        return confirmacion, pedido


application = Application([StoreService], 'spyne.tienda.soap',
                          in_protocol=Soap11(validator="lxml"),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
    server = make_server('0.0.0.0', 8000, wsgi_application)
    print("SOAP server is listening in: http://127.0.0.1:8000")
    print("WSDL is running in: http://127.0.0.1:8000/?wsdl")
    server.serve_forever() # Mantiene el servidor en ejecución