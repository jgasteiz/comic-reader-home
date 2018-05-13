from rest_framework import serializers

from reader.models import FileItem


class SimpleFileItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileItem
        fields = (
            'pk',
            'name',
            'path',
            'encoded_path',
            'file_type',
        )


class FileItemSerializer(serializers.ModelSerializer):
    children = SimpleFileItemSerializer(many=True)

    class Meta:
        model = FileItem
        fields = (
            'pk',
            'name',
            'path',
            'encoded_path',
            'file_type',
            'parent',
            'children',
            'num_pages',
        )
