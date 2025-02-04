from flask import Blueprint, render_template, flash, redirect, send_from_directory
from flask_login import login_required, current_user
from .forms import AddProductForm, AddEmployeeForm
from werkzeug.utils import secure_filename
from .models import Product, Employee, Customer
from . import db
import os



admin = Blueprint('admin', __name__)

@admin.route('/media/<path:filename>')
def get_image(filename):
    return send_from_directory('../media', filename)


@admin.route('/add_product', methods=['GET', 'POST'])
@login_required
def AddProduct():
    if current_user.id == 1:
        form = AddProductForm()
        if form.validate_on_submit():
            product_name = form.product_name.data
            previous_price = form.previous_price.data
            current_price = form.current_price.data
            flash_sale = form.flash_sale.data

            file = form.product_picture.data
            if file:
                file_name = secure_filename(file.filename)
                file_path = os.path.join(os.getcwd(), 'media', file_name)
                try:
                    file.save(file_path)
                    # Save product to the database
                    new_product = Product(
                        product_name=product_name,
                        previous_price=previous_price,
                        current_price=current_price,
                        flash_sale=flash_sale,
                        product_picture=f'/media/{file_name}',
                    )
                    db.session.add(new_product)
                    db.session.commit()
                    flash(f'{product_name} added successfully!')
                except Exception as e:
                    print(e)
                    flash('Failed to save product.')
            else:
                flash('No file selected for upload.')

        products = Product.query.order_by(Product.date_added.desc()).all()
        return render_template('add_product.html', form=form, products=products)

    return render_template('404.html')



@admin.route('/add_employee', methods=['GET', 'POST'])
@login_required
def AddEmployee():
    if current_user.id == 1:  # Check admin privileges
        form = AddEmployeeForm()
        if form.validate_on_submit():
            email = form.email.data
            employee_name = form.employee_name.data
            date_of_birth = form.date_of_birth.data
            gender = form.gender.data
            role = form.role.data
            date_added = form.date_added.data

            # Check for existing email
            existing_employee = Employee.query.filter_by(email=email).first()
            if existing_employee:
                flash('Employee with this email already exists.')
            else:
                # Create a new Employee instance
                new_employee = Employee(
                    email=email,
                    employee_name=employee_name,
                    date_of_birth=date_of_birth,
                    gender=gender,
                    role=role,
                    date_added=date_added,
                )

                try:
                    db.session.add(new_employee)
                    db.session.commit()
                    flash('Employee added successfully!')
                except Exception as e:
                    db.session.rollback()
                    print(e)
                    flash('Failed to add Employee.')

     
        employees = Employee.query.order_by(Employee.date_added.desc()).all()
        return render_template('add_employee.html', form=form, new_employees=employees)


    return render_template('404.html')


@admin.route('/shop-items', methods=['GET', 'POST'])
@login_required
def shop_items():
    if current_user.id == 1:
        items = Product.query.order_by (Product.date_added.desc()).all()
        return render_template('shop_items.html', items=items)
    return render_template('404.html')


@admin.route('/update_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def update_product(product_id):
    if current_user.id == 1:
        form = AddProductForm()

        item_to_update = Product.query.get(product_id)

        form.product_name.render_kw = {'placeholder': item_to_update.product_name}
        form.previous_price.render_kw = {'placeholder': item_to_update.previous_price}
        form.current_price.render_kw = {'placeholder': item_to_update.current_price}
        form.flash_sale.render_kw = {'placeholder': item_to_update.flash_sale}

        if form.validate_on_submit():
            product_name = form.product_name.data
            current_price = form.current_price.data
            previous_price = form.previous_price.data
            flash_sale = form.flash_sale.data

            file = form.product_picture.data

            file_name = secure_filename(file.filename)
            file_path = f'./media/{file_name}'

            file.save(file_path)

            try:
                Product.query.filter_by(id=product_id).update(dict(product_name=product_name,
                                                                current_price=current_price,
                                                                previous_price=previous_price,
                                                                flash_sale=flash_sale,
                                                                product_picture=file_path))

                db.session.commit()
                flash(f'{product_name} updated Successfully')
                print('Product Upadted')
                return redirect('/add_product')
            except Exception as e:
                print('Product not Upated', e)
                flash('Item Not Updated!!!')

        products = Product.query.order_by(Product.date_added.desc()).all()

        return render_template('update_product.html', form=form)
    return render_template('404.html')


@admin.route('/delete_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def delete_product(product_id):
    if current_user.id == 1:
        try:
            item_to_delete = Product.query.get(product_id)
            db.session.delete(item_to_delete)
            db.session.commit()
            flash('One product deleted')
            return redirect('/add_product')
        except Exception as e:
            print('Failed to delete product', e)
            flash('Failed to delete product!!')
        return redirect('/add_product')

    return render_template('404.html')


@admin.route('Update_employee/<int:employee_id>', methods=['GET', 'POST'])
@login_required
def delete_employee(employee_id):
    if current_user.id == 1:
        form = AddEmployeeForm()

        employee_to_update = Employee.query.get(employee_id)

        
    return render_template('404.html')


@admin.route('/customers')
@login_required
def display_customers():
    if current_user.id == 1:
        customers = Customer.query.all()
        return render_template('customers.html', customers=customers)
    return render_template('404.html')


@admin.route('/admin-page')
@login_required
def admin_page():
    if current_user.id == 1:
        return render_template('admin.html')
    return render_template('404.html')