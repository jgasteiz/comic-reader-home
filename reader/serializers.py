from rest_framework import serializers

from reader import models


class SimpleFileItemSerializer(serializers.ModelSerializer):
    bookmarked_page = serializers.SerializerMethodField()

    class Meta:
        model = models.FileItem
        fields = ("pk", "name", "path", "file_type", "bookmarked_page")

    def get_bookmarked_page(self, obj: models.FileItem):
        if hasattr(obj, "bookmark"):
            return obj.bookmark.page_number


class FileItemSerializer(serializers.ModelSerializer):
    children = SimpleFileItemSerializer(many=True)

    class Meta:
        model = models.FileItem
        fields = (
            "pk",
            "name",
            "path",
            "file_type",
            "parent",
            "children",
            "num_pages",
        )


class BookmarkSerializer(serializers.Serializer):
    comic_id = serializers.IntegerField()
    page_number = serializers.IntegerField()
