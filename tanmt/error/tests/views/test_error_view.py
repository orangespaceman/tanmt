from django.test import TestCase


class TestErrorView(TestCase):

    def test_get_404(self):
        """"
        GET request returns 404
        """
        url = '/lorem/ipsum'

        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'error/error.html')
