#!/bin/bash

# 1. Deploy de la aplicación en AWS utilizando Serverless
echo "Desplegando proyecto de Inti Luna en AWS usando serverless..."
serverless deploy

# 2 Esperar 3 segundos para que la URL de la API HTTP esté lista
echo "Esperando que la URL de la API HTTP esté disponible..."
sleep 3

# 3. Llamar a una función para rellenar la base de datos con registros de prueba
echo "Insertando registros de prueba en la base de datos..."
#api_url=$(sls info --verbose | grep HttpApiUrl | awk '{print $2}')
api_url=$(sls info --verbose | awk '/HttpApiUrl/{print $2}')
python preload_using_endpoint.py "$api_url"

# 4. Abriendo pagina web
echo "Abriendo la página web con la URL de la API HTTP: $api_url..."
echo "En caso de que no se abra automáticamente, abra manual en browser: $api_url..."

