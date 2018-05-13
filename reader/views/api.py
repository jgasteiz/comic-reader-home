from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from reader.models import FileItem
from reader.serializers import FileItemSerializer


class FileItemViewSet(viewsets.ModelViewSet):
    serializer_class = FileItemSerializer
    queryset = FileItem.objects.all()

    def list(self, request, **kwargs):
        queryset = self.queryset.filter(parent=None)
        serializer = self.serializer_class(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        file_item = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(file_item, context={'request': request})
        return Response(serializer.data)
