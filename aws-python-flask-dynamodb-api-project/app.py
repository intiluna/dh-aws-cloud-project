import os
import boto3
# import requests
from flask import Flask, jsonify, make_response, request, render_template

app = Flask(__name__)


dynamodb_client = boto3.client('dynamodb')

if os.environ.get('IS_OFFLINE'):
    dynamodb_client = boto3.client(
        'dynamodb', region_name='localhost', endpoint_url='http://localhost:8000'
    )


ANUNCIOS_TABLE = os.environ['ANUNCIOS_TABLE']

@app.route('/')
def index():
    return render_template('index.html')

# vista para mostrar formulario de nuevo anuncio
@app.route('/nuevo-anuncio')
def mostrar_formulario_nuevo_anuncio():
    return render_template('anuncio_nuevo.html')


# Endpoint de vista de detalle de anuncio
@app.route('/anuncios/<string:anuncio_id>')
def get_anuncio_detalle(anuncio_id):
    result = dynamodb_client.get_item(
        TableName=ANUNCIOS_TABLE, Key={'anuncioId': {'S': anuncio_id}}
    )
    item = result.get('Item')
    if not item:
        return jsonify({'error': 'No pude encontrar anuncio con ese "anuncioID"'}), 404

    anuncio = {
        'anuncioId': item.get('anuncioId').get('S'),
        'titulo': item.get('titulo').get('S'),
        'precio': item.get('precio').get('S'),
        'email': item.get('email').get('S'),
    }

    return render_template('detalle_anuncio.html', libro=anuncio)


# Endpoint para eliminar un anuncio por su ID
@app.route('/anuncios/<string:anuncio_id>', methods=['DELETE'])
def delete_anuncio(anuncio_id):
    # Primero, verifica si el anuncio existe
    result = dynamodb_client.get_item(
        TableName=ANUNCIOS_TABLE, Key={'anuncioId': {'S': anuncio_id}}
    )
    item = result.get('Item')
    if not item:
        return jsonify({'error': 'No pude encontrar anuncio con ese "anuncioID"'}), 404

    # Si el anuncio existe, procede a eliminarlo
    dynamodb_client.delete_item(
        TableName=ANUNCIOS_TABLE, Key={'anuncioId': {'S': anuncio_id}}
    )

    return jsonify({f'message': 'Anuncio {anuncio_id} eliminado exitosamente'}), 200   

# Crear nuevo anuncio
@app.route('/anuncio-nuevo', methods=['POST'])
def create_anuncio():
    anuncio_id = request.json.get('anuncioId')
    titulo = request.json.get('titulo')
    precio = request.json.get('precio')
    email = request.json.get('email')
    if not anuncio_id or not titulo or not precio:
        return jsonify({'error': 'Por favor brinde: "anuncioId", "titulo", "precio", "email"'}), 400

    dynamodb_client.put_item(
        TableName=ANUNCIOS_TABLE, Item={'anuncioId': {'S': anuncio_id}, 'titulo': {'S': titulo}, 'precio': {'S': precio}, 'email': {'S': email}}
    )

    return jsonify({'anuncioId': anuncio_id, 'titulo': titulo}),200


# Listar anuncios
@app.route('/anuncios', methods=['GET'])
def get_list_anuncios():
    try:
        response = dynamodb_client.scan(
            TableName=ANUNCIOS_TABLE
        )
        items = response.get('Items', [])
        if not items:
            #return jsonify({'message': 'No hay anuncios en la tabla'}), 404
            return render_template('no_hay_anuncios.html'), 400

        anuncios = []
        for item in items:
            anuncio = {
                'anuncioId': item.get('anuncioId').get('S'),
                'titulo': item.get('titulo').get('S')
            }
            anuncios.append(anuncio)

        #return jsonify(anuncios), 200
        return render_template('anuncios.html', anuncios=anuncios), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)


# if __titulo__ == "__main__":
#     # Preload data into DynamoDB
#     from preload_db import upload_records_from_csv
#     # Ensure that preload_db.py is run only when this script is executed directly
#     upload_records_from_csv(os.path.join(os.path.dirtitulo(__file__), 'records_to_populate_db.csv'))
#     app.run(debug=True)
