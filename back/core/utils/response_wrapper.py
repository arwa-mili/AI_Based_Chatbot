from rest_framework.response import Response
from rest_framework import status

def api_response(success=True, info="", data=None, error=None, status_code=status.HTTP_200_OK):
    return Response(
        {
            "success": success,
            "info": info,
            "data": data,
            "error": error,
        },
        status=status_code,
    )
