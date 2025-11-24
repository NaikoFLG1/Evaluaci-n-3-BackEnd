from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection

class DBHealthView(APIView):
    permission_classes = []  

    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            row = cursor.fetchone()
        return Response({"db": "ok" if row and row[0] == 1 else "error"})
