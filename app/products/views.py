
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from flask import (
    render_template, redirect, url_for,
    flash, request, abort, current_app
)
from werkzeug.utils import secure_filename

from . import products_bp
from .db import products_table
from .forms import ProductForm


UPLOAD_DIR = Path(__file__).resolve().parent / 'static' / 'uploads'
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_image(image):
    if not image or not image.filename:
        return None

    filename = secure_filename(image.filename)
    extension = Path(filename).suffix.lower()

    if extension not in ['.jpg', '.jpeg', '.png']:
        return None

    new_filename = f'{uuid4().hex}{extension}'
    image.save(UPLOAD_DIR / new_filename)

    return f'uploads/{new_filename}'


@products_bp.route('/')
def product_list():
    products = products_table.all()

    return render_template(
        'products/products.html',
        title='Список товарів',
        products=products
    )


@products_bp.route('/<int:product_id>')
def product_detail(product_id):
    product = products_table.get(doc_id=product_id)

    if product is None:
        abort(404)

    return render_template(
        'products/detail_product.html',
        title=product['name'],
        product=product
    )


@products_bp.route('/add', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()

    if form.validate_on_submit():
        image_path = save_image(form.image.data)

        product = {
            'name': form.name.data,
            'content': form.content.data,
            'price': str(form.price.data),
            'category': form.category.data,
            'quantity': form.quantity.data,
            'image': image_path,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        product_id = products_table.insert(product)
        products_table.update({'id': product_id}, doc_ids=[product_id])

        flash('Товар успішно додано!', 'success')
        return redirect(url_for('products.product_list'))

    if form.is_submitted() and form.errors:
        flash('Перевірте правильність заповнення форми.', 'danger')

    return render_template(
        'products/product_form.html',
        title='Додати товар',
        form=form,
        heading='Додати товар'
    )
