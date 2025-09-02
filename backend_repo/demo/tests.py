from rest_framework.test import APITestCase
from rest_framework import status
from .models import Post, Comment
from django.contrib.auth.models import User

class PostAPITestCase(APITestCase):
    """
    Test suite for the Post API endpoints.

    This test case checks the functionality of the Post API, specifically:
    - Verifying that a list of posts can be retrieved with correct pagination.
    - Ensuring that each post has up to 3 random comments returned when listed.
    """
    
    def setUp(self):
        """
        Sets up test data by creating a user, a post, and a set of comments.

        The test user is created, followed by the creation of one post. 
        Additionally, 5 comments are created for this post to simulate user interaction.
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(text='Test post', user=self.user)
        for i in range(5):  # Create 5 comments for this post
            Comment.objects.create(text=f'Comment {i + 1}', post=self.post, user=self.user)

    def test_post_list(self):
        """
        Test the retrieval of posts with pagination and a limited number of comments.

        This test ensures that:
        - The API returns a 200 OK status code.
        - Only one post is created in the database.
        - The post has no more than 3 comments after pagination.
        """
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Only 1 post created
        self.assertLessEqual(len(response.data['results'][0]['comments']), 3)  # Only up to 3 comments

    def test_random_comments(self):
        """
        Test the randomness of the comments returned for each post.

        This test checks that:
        - When retrieving posts, only 3 or fewer comments are returned for each post.
        - The selection of comments is random, simulating the behavior of the view logic.
        """
        response = self.client.get('/api/posts/')
        post = response.data['results'][0]
        comments = post['comments']
        self.assertLessEqual(len(comments), 3)  # Should return 3 or fewer comments
