from django.test import TestCase
from django.urls import reverse
from .models import Thread, Post

# Create your tests here.
class TestBoard(TestCase):

    def setUp(self):
        self.thread = Thread.objects.create(title='test', user_id='test', is_archived=0)
        self.post = Post.objects.create(thread=self.thread, content='Test Post', user_id="4556575")

    def test_thread_list(self):
        url = reverse('thread_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'board/thread_list.html')
        self.assertContains(response, 'test')


    def test_thread_detail(self):
        url = reverse('thread_detail', args=[self.thread.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'board/thread_detail.html')
        self.assertContains(response, 'Test Post')

    def test_thread_create(self):
        url = reverse('thread_list')
        response = self.client.post(url, {'title': 'test', 'user_id': 'test'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Thread.objects.count(), 2)

    def test_post_create(self):
        url = reverse('thread_list')
        response = self.client.post(url, {'title': 'test', 'user_id': 'test'})
        url2 = reverse('thread_detail', args=[self.thread.pk])
        response = self.client.post(url2, {'content': 'Test Post', 'user_id': 'test'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 2)