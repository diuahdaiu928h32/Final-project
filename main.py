from flask import Flask, request, render_template, make_response, redirect, url_for

app = Flask(__name__, template_folder='templates')

# Cargar claves desde el archivo key.txt
with open('key.txt', 'r') as file:
    claves_autorizadas = {line.strip() for line in file}

@app.route('/')
def index():
    # Verificar si ya se ha verificado mediante cookies
    verified = request.cookies.get('verified')
    if verified == 'true':
        return render_template('authorized.html')

    return render_template('index.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    entered_key = request.form.get('entered_key')
    # Verificar si la clave ingresada está autorizada
    if entered_key in claves_autorizadas:
        # Eliminar la clave verificada de la lista
        claves_autorizadas.remove(entered_key)
        # Actualizar el archivo key.txt con las claves restantes
        with open('key.txt', 'w') as file:
            file.write('\n'.join(claves_autorizadas))
        # Establecer cookie para indicar que se ha verificado
        response = make_response(redirect(url_for('index')))
        response.set_cookie('verified', 'true')
        response.set_cookie('authenticatedUser', 'DANI')  # Almacena el nombre del usuario
        return response
    else:
        # Si la clave es incorrecta, muestra el mensaje de error
        return 'La clave no es correcta. Contacta con el creador "DANI".'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
