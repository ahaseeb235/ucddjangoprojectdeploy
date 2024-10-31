# blog/tests.py
# https://github.com/UCD-Full-Stack-Jan-2024/Frameworks/blob/main/Week5/unit10/Unit_10_Walkthrough_Testing.py

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post



# create your tests here:

class PostModelTests(TestCase):
    @classmethod
    def setUpTestData(cls): # cll = class level setup
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.post = Post.objects.create(
            author=cls.user,
            title='Test Post',
            content='This is a test post'
        )
        
    #2. test_post_content method
    def test_post_content(self):
        post = Post.objects.get(id=1)
        expected_author = f'{post.author}'
        expected_title = f'{post.title}'
        expected_content = f'{post.content}'
        self.assertEqual(expected_author, 'testuser')
        self.assertEqual(expected_title, 'Test Post')
        self.assertEqual(expected_content, 'This is a test post')
        
    
    #3.  test_post_str_method method
    def test_post_str_method(self):
        post = Post.objects.get(id=1)
        self.assertEqual(str(post), post.title)

    #4.  test_get_absolute_url method
    def test_get_absolute_url(self):
        post = Post.objects.get(id=1)
        self.assertEqual(post.get_absolute_url(), reverse('post-detail', args=[post.id]))

# 5.  setUp method
class PostViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='This is a test post'
        )
    
    #6.  test_post_list_view method
    def test_post_list_view(self):
        url = reverse('blog-home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is a test post')
        self.assertTemplateUsed(response, 'blog/home.html')
        
    #7.  test_post_detail_view method
    def test_post_detail_view(self):
        url = reverse('post-detail', args=[self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.content)
        self.assertContains(response, self.user.username)
        # self.assertContains(response, self.user.password) # password testing does not work
        

# 8.  test_create_post_view method

    def test_create_post_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('post-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_form.html')

        response = self.client.post(reverse('post-create'), {
            'title': 'New title',
            'content': 'New text',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after POST
        self.assertTrue(Post.objects.filter(title='New title').exists())
        
#9.  test_update_post_view method

    def test_update_post_view(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('post-update', kwargs={'pk': self.post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_form.html')

        response = self.client.post(url, {
            'title': 'Updated title',
            'content': 'Updated text',
        })
        self.post.refresh_from_db()
        self.assertEqual(response.status_code, 302)  # Redirect after POST
        self.assertEqual(self.post.title, 'Updated title')
        self.assertEqual(self.post.content, 'Updated text')
        
    # 10. test_delete_post_view method

    def test_delete_post_view(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('post-delete', kwargs={'pk': self.post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_confirm_delete.html')

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirect after POST
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())