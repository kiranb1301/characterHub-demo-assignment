# TODO There's certainly more than one way to do this task, so take your pick.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment
from .serializers import PostSerializer
import random

class PostPagination(PageNumberPagination):
    page_size = 10  
    page_size_query_param = 'page_size'  

class PostViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and managing blog posts.
    It also implements custom pagination and displays a random selection of up to 3 comments per post when listing posts.

    The `list` action returns a paginated list of posts with a limited number of comments (3 or fewer) per post.
    """

    queryset = Post.objects.all().order_by('-timestamp')  
    serializer_class = PostSerializer
    pagination_class = PostPagination

    def list(self, request, *args, **kwargs):
        """
        Retrieves a paginated list of posts with a random selection of comments for each post.

        This method overrides the default `list` behavior to ensure:
        - Posts are ordered by timestamp (most recent first).
        - Each post contains up to 3 random comments (if available), ensuring that each post appears with a manageable number of comments.
        
        Pagination is applied to limit the number of posts returned per page, which is defined by the `PostPagination` class.

        Args:
            request: The HTTP request object containing query parameters such as pagination settings.

        Returns:
            Response: A paginated response containing serialized data of the posts and their respective comments.
        """
        
        posts = self.get_queryset()

        for post in posts:
            comments = list(post.comments.all())
            random_comments = random.sample(comments, 3) if len(comments) >= 3 else comments
            post.comments.set(random_comments)  

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(posts, request)
        
        serializer = self.get_serializer(result_page, many=True)
        
        return paginator.get_paginated_response(serializer.data)
