import boto3
import botocore
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
from flask import Flask, request

import base64
import tempfile
import uuid
import logging
import creds

app = Flask(__name__)

@app.route('/')
def home():
   return '¡Hola Mundo!'

@app.route('/tarea3-201603016', methods = ['POST'])
def rekognition_tarea3():
    if request.method == 'POST':
        content = request.get_json()
        imagen = content['imagen']
    
        rekognition_client = boto3.client(
            'rekognition',
            aws_access_key_id=creds.rekognition['access_key_id'],
            aws_secret_access_key=creds.rekognition['secret_access_key'],
            region_name=creds.rekognition['region'],
        )

        try:
            response = rekognition_client.detect_labels(
               Image ={
                   'Bytes': base64.b64decode(imagen)

               },
               MaxLabels = 123

            )
            logging.info(response)
            return response
        except ClientError as e:
            logging.error(e)
            return e.response

if __name__ == '__main__':
   app.run(host='0.0.0.0', debug=True)
