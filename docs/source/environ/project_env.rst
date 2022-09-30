.. code-block:: yaml

   version: "3.7"

   x-variables: &variables
     ENV_STAGE: dev
     USE_HTTPS: 0

   services:
     web:
       ports:
         - "9000:8000"
       environment:
         <<: *variables
     celery:
       environment:
         <<: *variables

   networks:
     microservice_network:
       name: dev_microservice_network

