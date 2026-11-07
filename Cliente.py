from zeep import Client

wsdl_url = 'http://127.0.0.1:8000/?wsdl'

try:
    cliente = Client(wsdl=wsdl_url)
    print("Cliente conectado al WSDL", wsdl_url)
    
    resultado_suma = cliente.service.sumar(5, 5)
    print("Resultado de la suma:", resultado_suma)

    resultado_resta = cliente.service.restar(5, 5)
    print("Resultado de la resta:", resultado_resta)

    resultado_division = cliente.service.dividir(8, 7)
    print("Resultado de la división:", resultado_division)

    resultado_multiplicacion = cliente.service.multiplicar(8, 2)
    print("Resultado de la multiplicación:", resultado_multiplicacion)

    # Try catches de cada excepción, para que no se detenga la ejecución del cliente.
    try:
        resultado_division_cero = cliente.service.dividir(8, 0)
        print("Resultado de la división por cero:", resultado_division_cero)
    except Exception as e:
        print("Error al dividir entre cero:", e)

except Exception as e:
    print("Error al conectar con el WSDL:", e)