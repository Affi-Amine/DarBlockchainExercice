from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Book
from .serializers import BookSerializer
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
import requests
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView


class BookCreateView(APIView):
    @swagger_auto_schema(
        operation_description="Create a new book with the provided details.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description="The title of the book. Must be unique and between 1-255 characters."),
                'author': openapi.Schema(type=openapi.TYPE_STRING, description="The author of the book. Must be between 1-255 characters."),
                'genre': openapi.Schema(type=openapi.TYPE_STRING, description="The genre of the book. Must be one of: Fiction, Non-Fiction, Mystery, Sci-Fi, Fantasy."),
                'cover_image': openapi.Schema(type=openapi.TYPE_STRING, description="The URL of the book's cover image. Optional."),
            },
            required=['title', 'author']
        ),
        responses={
            201: openapi.Response(
                description="Book created successfully",
                schema=BookSerializer
            ),
            400: "Bad Request - Invalid data",
        },
        security=[{"Bearer": []}]
    )
    def post(self, request):
        """
        Create a new book with the provided details.
        """
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = PageNumberPagination

    @swagger_auto_schema(
        operation_description="Retrieve a paginated list of all books.",
        manual_parameters=[
            openapi.Parameter(
                name='page',
                in_=openapi.IN_QUERY,
                description="Page number to retrieve.",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                name='limit',
                in_=openapi.IN_QUERY,
                description="Number of books per page.",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
        ],
        responses={
            200: openapi.Response(
                description="Paginated list of books",
                schema=BookSerializer(many=True)
            ),
            400: "Invalid page or limit value",
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class BookDetailView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'id'  # Use 'id' to retrieve the book

    @swagger_auto_schema(
        operation_description="Retrieve details for a specific book by ID.",
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                description="The ID of the book to retrieve.",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Book details",
                schema=BookSerializer
            ),
            404: "Book not found",
        }
    )
    def get(self, request, *args, **kwargs):
        # Fetch the book from the database
        book = self.get_object()

        # Fetch additional metadata from Google Books API
        google_books_data = self.fetch_google_books_metadata(book.title, book.author)

        # Combine the internal and external data
        response_data = self.serializer_class(book).data
        response_data['google_books_metadata'] = google_books_data

        return Response(response_data, status=status.HTTP_200_OK)

    def fetch_google_books_metadata(self, title, author):
        """
        Fetch metadata from Google Books API.
        """
        base_url = "https://www.googleapis.com/books/v1/volumes"
        query = f"intitle:{title}+inauthor:{author}"
        params = {
            'q': query,
            'maxResults': 1  # Fetch only the first result
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()

            if data.get('totalItems', 0) > 0:
                # Extract relevant metadata from the first result
                book_info = data['items'][0]['volumeInfo']
                return {
                    'description': book_info.get('description', 'No description available'),
                    'published_date': book_info.get('publishedDate', 'Unknown'),
                    'publisher': book_info.get('publisher', 'Unknown'),
                    'average_rating': book_info.get('averageRating', 'Not rated'),
                    'ratings_count': book_info.get('ratingsCount', 0),
                    'thumbnail': book_info.get('imageLinks', {}).get('thumbnail', 'No thumbnail available')
                }
            else:
                return {"error": "No matching book found in Google Books"}
        except requests.RequestException as e:
            return {"error": f"Failed to fetch metadata from Google Books: {str(e)}"}
        
class BookUpdateView(UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'id'  

    @swagger_auto_schema(
        operation_description="Update details for a specific book by ID.",
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                description="The ID of the book to update.",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        request_body=BookSerializer,
        responses={
            200: openapi.Response(
                description="Book updated successfully",
                schema=BookSerializer
            ),
            400: "Invalid data",
            404: "Book not found",
        }
    )
    def patch(self, request, *args, **kwargs):
        """
        Partially update a book's details.
        """
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Fully update a book's details.
        """
        return self.update(request, *args, **kwargs)
    
class BookDeleteView(DestroyAPIView):
    queryset = Book.objects.all()
    lookup_field = 'id'  
    permission_classes = [IsAdminUser]  

    @swagger_auto_schema(
        operation_description="Delete a specific book by ID.",
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                description="The ID of the book to delete.",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            204: "Book deleted successfully",
            403: "Permission denied - Only admins can delete books",
            404: "Book not found",
        }
    )
    def delete(self, request, *args, **kwargs):
        """
        Delete a book by ID.
        """
        return self.destroy(request, *args, **kwargs)
