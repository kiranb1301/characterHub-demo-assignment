from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth.models import User

# TODO There's certainly more than one way to do this task, so take your pick.
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'text', 'timestamp', 'author']

class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model.

    This serializer is used to:
    - Return post details including the author's username and the count of comments.
    - Include up to 3 random comments associated with the post.
    """
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)
    comments = serializers.SerializerMethodField()
    author = serializers.CharField(source='user.username')

    class Meta:
        model = Post
        fields = ['id', 'text', 'timestamp', 'author', 'comment_count', 'comments']

    def get_comments(self, obj):
        comments = obj.comments.order_by('?')[:3]
        return CommentSerializer(comments, many=True).data
