# TODO There's certainly more than one way to do this task, so take your pick.
# backend_repo/apps/demo/serializers.py
from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth.models import User

# Serializer for the Comment model
class CommentSerializer(serializers.ModelSerializer):
    # Include the username of the comment's author
    author = serializers.CharField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'text', 'timestamp', 'author']

class PostSerializer(serializers.ModelSerializer):
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)
    comments = serializers.SerializerMethodField()   # 👈 override here
    author = serializers.CharField(source='user.username')

    class Meta:
        model = Post
        fields = ['id', 'text', 'timestamp', 'author', 'comment_count', 'comments']

    def get_comments(self, obj):
        # Return at most 3 random comments
        comments = obj.comments.order_by('?')[:3]
        return CommentSerializer(comments, many=True).data
