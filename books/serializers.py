from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        max_length=255,
        help_text="The title of the book. Must be unique and between 1-255 characters."
    )
    author = serializers.CharField(
        max_length=255,
        help_text="The author of the book. Must be between 1-255 characters."
    )
    genre = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        help_text="The genre of the book. Must be one of: Fiction, Non-Fiction, Mystery, Sci-Fi, Fantasy."
    )
    cover_image = serializers.URLField(
        required=False,
        allow_blank=True,
        help_text="The URL of the book's cover image. Optional."
    )

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre', 'cover_image']

    def validate_genre(self, value):
        allowed_genres = ['Fiction', 'Non-Fiction', 'Mystery', 'Sci-Fi', 'Fantasy', 'Dystopian']
        if value and value not in allowed_genres:
            raise serializers.ValidationError(f"Genre '{value}' is not allowed.")
        return value