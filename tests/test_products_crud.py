
import unittest
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from tinydb import TinyDB

from app import app
from app.products import views


class TestProductsCRUD(unittest.TestCase):

    def setUp(self):
        self.temp_dir = TemporaryDirectory()

        self.db = TinyDB(
            Path(self.temp_dir.name) / 'test_products.json'
        )

        self.table = self.db.table('products')

        self.table_patch = patch.object(
            views, 'products_table', self.table
        )
        self.table_patch.start()

        app.config.update(
            TESTING=True,
            WTF_CSRF_ENABLED=False
        )

        self.client = app.test_client()

        self.product_data = {
            'name': 'Laptop',
            'content': 'Test laptop description',
            'price': '1200.50',
            'category': 'laptops',
            'quantity': '5'
        }

    def tearDown(self):
        self.table_patch.stop()
        self.db.close()
        self.temp_dir.cleanup()

    def create_product(self):
        response = self.client.post(
            '/product/add',
            data=self.product_data,
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.table), 1)

        return self.table.all()[0]['id']

    def test_create_product(self):
        product_id = self.create_product()

        product = self.table.get(doc_id=product_id)

        self.assertEqual(product['name'], 'Laptop')
        self.assertEqual(product['price'], '1200.50')
        self.assertEqual(product['quantity'], 5)
        self.assertIn('created_at', product)

    def test_read_products(self):
        self.create_product()

        response = self.client.get('/product/')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Laptop', response.data)

    def test_read_product_details(self):
        product_id = self.create_product()

        response = self.client.get(
            f'/product/{product_id}'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test laptop description', response.data)

    def test_update_product(self):
        product_id = self.create_product()

        updated_data = self.product_data.copy()
        updated_data['name'] = 'Updated Laptop'
        updated_data['price'] = '1500.00'

        response = self.client.post(
            f'/product/{product_id}/edit',
            data=updated_data,
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)

        product = self.table.get(doc_id=product_id)

        self.assertEqual(product['name'], 'Updated Laptop')
        self.assertEqual(product['price'], '1500.00')

    def test_delete_product(self):
        product_id = self.create_product()

        response = self.client.post(
            f'/product/{product_id}/delete',
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.table), 0)

    def test_invalid_product(self):
        invalid_data = self.product_data.copy()
        invalid_data['name'] = 'AB'
        invalid_data['price'] = '-10'

        response = self.client.post(
            '/product/add',
            data=invalid_data
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.table), 0)

    def test_product_not_found(self):
        response = self.client.get('/product/999999')

        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
