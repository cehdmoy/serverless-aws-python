# Como iniciar desde cero una función Serverless

 Para el desarrollo de las funciones serverless estaremos utilizando serverless framework por lo que para ello debemos tener los siguientes programas instalados:

 

- Node JS: https://nodejs.dev/
- Serverless: https://www.serverless.com/framework/docs/getting-started#via-npm
- Python: https://www.python.org/downloads/
- AWS-CLI: https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html



tambien utilizaremos python como lenguaje principal, las funciones pueden ser probadas de forma local pero se recomienda hacer pruebas en ambiente de desarrollo AWS para verificar que las librerías python requeridas se instalen correctamente durante el despliegue gestionado por serverless.

 

## Preparación de ambiente local:

Serverless framework (en adelante sls) ofrece herramientas de administración y monitoreo a funciones serverless. 

En caso de se quiera tener acceso al dashboard de sls, se debe iniciar sesión a través del siguiente comando:


```
sls login
```


Para que sls tenga acceso a las herramientas de amazon se debe iniciar sesión en amazon a través de la línea de comandos de AWS-CLI


```
aws configure
```
 
---
**Dato:**

Para mayor detalle de como configurar la sesión de aws revisar la siguiente documentación: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html

---
 

Creación aplicación base:
 

Para iniciar debemos crear una carpeta nueva en donde queremos que quede todo nuestro código y las definiciones de las funciones lambda a desplegar.

Se pueden  definir varias funciones lambda en un mismo proyecto sls

 

Dentro de la carpeta debemos ejecutar el siguiente comando:


```
npm init -f
```
 

Una vez inicializado el proyecto, ejecutamos el siguiente comando para instalar la librería sls que nos ayudará a gestionar los requerimientos python al desplegar:


```
npm install --save-dev serverless-python-requirements
```
 

Ahora debemos crear nuestro archivo de definición sls (serverless.yml) con el siguiente contenido:

```

service: example

plugins:
  - serverless-python-requirements

package:
  exclude:
    - node_modules/**
    - .idea/**
    - .requirements/**
    - env/**
    - README.md
    - package.json
    - package-lock.json
    - requirements.txt
    
custom:
  parameters:
    apiUrl: ${opt:apiUrl, self:custom.defaults-parameters-values.apiUrl}
  defaults-parameters-values:
    apiUrl: "https://jsonplaceholder.typicode.com/todos/1"


provider:
  name: aws
  runtime: python3.8

functions:
  main:
    handler: src/handler.main
    events:
      - http:
          path: /
          method: get
    environment:
      API_URL: ${self:custom.parameters.apiUrl}
```
 
---
**Dato:**

Para usar el dashboard de sls, se debe crear la aplicacion primero en el sitio serverless.com y agregar lo siguiente al inicio de serverless.yml:

org: consorcio
app: example

---
 

Una vez especificadas las configuraciones en serverless.yml, debemos desarrollar la función de entrada al método que queremos exponer, este código se almacenará en el archivo handler.py y para mantener organizado los archivos lo crearemos dentro de una carpeta llamada src

 
```


import json
import os
from aiohttp import request

import asyncio

loop = asyncio.get_event_loop()

async def get(url, headers):
    async with request('GET', url, headers=headers) as response:
        
        if response.status > 300:
            raise Exception(await response.text())
        
        return  await response.json()

async def main_async(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event,
        "request-response": await get(os.environ['API_URL'], {}) 
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

def main(event, context):   
    return loop.run_until_complete(main_async(event, context))

 
```

Terminado el desarrollo, debemos instalar las dependencias en un entorno privado virtual de python para poder desplegar la función:

```

virtualenv venv --python=python3
source venv/bin/activate
```

---
**Dato:**

En el siguiente enlace pueden conseguir mayor detalle de entornos virtuales en python: https://docs.python.org/3/tutorial/venv.html

---
 

Como nuestro código hace uso de la librería aiohttp, debemos instalarla y congelar la versión en nuestro archivo requirements.txt  ejecutando los siguientes comando en la raíz del proyecto:


```
pip install aiohttp
pip freeze > requirements.txt
```

Adicionalmente nuestro código hace uso de la librería asyncio para poder ejecutar los métodos de forma asíncrona internamente, aun así no hace falta incluirlo en el comando anterior ya que es una librería de python al igual que json

 

Una vez instaladas las librerías, se despliega el servicio con el siguiente comando:


```
sls deploy
```
 

El resultado del comando exitoso debe mostrar lo siguiente:

```

Serverless: Stack update finished...
Service Information
service: example
stage: dev
region: us-east-1
stack: example-dev
resources: 17
api keys:
  None
endpoints:
  GET - https://XXXXXX.execute-api.us-east-1.amazonaws.com/dev/
functions:
  main: example-dev-main
layers:
  None
Serverless: Publishing service to the Serverless Dashboard...
```

Donde “https://XXXXXX.execute-api.us-east-1.amazonaws.com/dev/”  es nuestro nuevo endpoint

 

En caso de querer probar la funcion de forma local, se puede invocar con el siguiente comando:


```
serverless invoke local --function main
```