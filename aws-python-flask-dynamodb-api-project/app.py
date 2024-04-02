import os
import boto3
# import requests
from datetime import datetime, timezone
from flask import Flask, jsonify, make_response, request, render_template
from boto3.dynamodb.conditions import Key


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

    return jsonify({'message': 'Anuncio eliminado exitosamente'}), 200   

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


# intentamos integrar funciones del chat
#Instancia de la tabla de mensajes
messages_table = boto3.resource('dynamodb').Table(os.environ.get('DYNAMODB_MESSAGES_TABLE'))

# Función para obtener los mensajes de un chat
def get_messages(chat_id):
    """Return the messages published in the chat room

    :param chat_id: ID of the chat
    :type chat_id: str

    :rtype: dict
        return example:
        {
            "messages": [
                {   "ts": "timestamp",   "user_id"": "author1",   "text": "text message"   },
                ...
            ]
        }
    """
    messages = messages_table.query(KeyConditionExpression=Key('chat_id').eq(chat_id))
    if "Items" in messages:
        return {'status': 200, 'messages': [{'ts': x['ts'], 'user_id': x['user_id'], 'text': x['text']} for x in messages["Items"]]}
    else:
        return {'status': 404, 'title': 'Chat not found', 'detail': f'Chat {chat_id} not found in database'}

# Función para enviar un mensaje a un chat
def send_message(chat_id, message):
    """Send a message into a chat room

    :param chat_id: ID of the chat
    :type chat_id: str
    :param message: new info
    :type message: dict
        message example:
        {
            "user_id": "user ID of the author",
            "text": "content written by the user",
        }

    :rtype: SimpleResponse
    """
    messages_table.put_item(
        Item={
            'chat_id': chat_id,
            'ts': datetime.now().replace(tzinfo=timezone.utc).isoformat(),
            'user_id': message['user_id'],
            'text': message['text'],
        }
    )
    return {'status': 201, 'title': 'OK', 'detail': f'New message posted into chat {chat_id}'}

# Endpoint para obtener los mensajes de un chat específico
@app.route('/chat/<string:chat_id>', methods=['GET'])
def get_chat_messages(chat_id):
    result = get_messages(chat_id)
    return jsonify(result)

# Endpoint para enviar un mensaje a un chat específico
@app.route('/chat/<string:chat_id>', methods=['POST'])
def post_chat_message(chat_id):
    message = request.json
    result = send_message(chat_id, message)
    return jsonify(result)



@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)


# if __titulo__ == "__main__":
#     # Preload data into DynamoDB
#     from preload_db import upload_records_from_csv
#     # Ensure that preload_db.py is run only when this script is executed directly
#     upload_records_from_csv(os.path.join(os.path.dirtitulo(__file__), 'records_to_populate_db.csv'))
#     app.run(debug=True)
