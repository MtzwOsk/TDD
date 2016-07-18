from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()  # 1
        response = home_page(request)  # 2
        expected_html = render_to_string('home.html')
        self.assertTrue(response.content.decode(), expected_html)
        self.assertTrue(response.content.startswith(b'<html>'))  # 3
        self.assertIn(b'<title>To-Do lists</title>', response.content)  # 4
        self.assertTrue(response.content.endswith(b'</html>'))  # 5

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        respnose = home_page(request)

        self.assertIn('A new list item', respnose.content.decode())
        expected_html = render_to_string(
            'home.html',
            {'new_item_text': 'A new list item'}
        )
        self.assertEqual(respnose.content.decode(), expected_html)
