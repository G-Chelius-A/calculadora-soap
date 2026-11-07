from zeep import Client
from zeep.exceptions import Fault

wsdl_url = 'http://127.0.0.1:8000/?wsdl'

try:
    cliente = Client(wsdl=wsdl_url)
    print("Cliente conectado al WSDL:", wsdl_url)
    
    pedido_valido = cliente.service.registrar_pedido(
        pedido = {
            "cliente": "Gerardo Chelius",
            "linea": [
                {"producto": "P001", "cantidad": 2},
                {"producto": "P002", "cantidad": 1}
            ]
        }

    )
    print("Pedido válido y confirmación:", pedido_valido)

    # Comprueba que se sumen las líneas repetidas antes de validar el stock.
    try:
        lineas_duplicadas = cliente.service.registrar_pedido(
            pedido={
                "cliente": "Cliente de prueba",
                "linea": [
                    {"producto": "P001", "cantidad": 5},
                    {"producto": "P001", "cantidad": 4}
                ]
            }
        )
        print("Pedido con líneas duplicadas y confirmación:", lineas_duplicadas)
    except Fault as e:
        print("Error al registrar pedido con líneas duplicadas:", e)

    try:
        stock_insuficiente = cliente.service.registrar_pedido(
            pedido = {
                "cliente": "Doctor Doom",
                "linea": [{"producto": "P001", "cantidad": 99}]
            }
        )
        print("Pedido con stock insuficiente y confirmación:", stock_insuficiente)
    except Fault as e:
        print("Error al registrar pedido con stock insuficiente:", e)

    try:
        producto_inexistente = cliente.service.registrar_pedido(
            pedido = {
                "cliente": "Thanos",
                "linea": [{"producto": "P999", "cantidad": 1}]
            }
        )
        print("Pedido con producto inexistente y confirmación:", producto_inexistente)
    except Fault as e:
        print("Error al registrar pedido con producto inexistente:", e)

    consulta = cliente.service.consultar_pedido(1)
    print("Consulta de pedido válido:", consulta)

    try:
        consulta_inexistente = cliente.service.consultar_pedido(50)
        print("Consulta de pedido inexistente:", consulta_inexistente)
    except Fault as e:
        print("Error al consultar pedido inexistente:", e)

    try:
        pedido_sin_linea = cliente.service.registrar_pedido(
            pedido = {
                "cliente": "Ultron",
                "linea": []
            }
        )
        print("Pedido sin líneas y confirmación:", pedido_sin_linea)
    except Fault as e:
        print("Error al registrar pedido sin líneas:", e)

    try:
        pedido_sin_cliente = cliente.service.registrar_pedido(
            pedido = {
                "cliente": "",
                "linea": [{"producto": "P001", "cantidad": 1}]
            }
        )
        print("Pedido sin cliente y confirmación:", pedido_sin_cliente)
    except Fault as e:
        print("Error al registrar pedido sin cliente:", e)

except Exception as e:
    print("Error al conectar al servidor WSDL:", e)