"""
Swagger API documentation settings.

It describes, what types of request and responses accept to endpoint.

For more information on this file, see
https://drf-yasg.readthedocs.io/en/stable/custom_spec.html

Example:
    response_schema_dict = {
        "200": openapi.Response(
            description="Successful information retrieving",
            schema=serializers.ResponseSerializer()
        ),
        "404": openapi.Response(
            description="Response, when information is invalid.",
            examples={
                "application/json": {
                    "detail": "Not found."
                }
            }
        )
    }
"""
from drf_yasg import openapi

from . import serializers
