from django.test import TestCase


class StoreViewTest(TestCase):
    def setUp(self):
        pass

    def test_index(self):
        resp = self.client.get('/store/')
        self.assertEqual(resp.status_code, 200)

    def test_detail_view(self):
        resp = self.client.get('/store/book/1/')
        self.assertEqual(resp.status_code, 404)

    def test_cart(self):
        resp = self.client.get('/store/cart/')
        self.assertEqual(resp.status_code, 302)
