
# Django Recap

Today we covered the beginning of how to use django. So far we've covered how to:

[Preface - make sure that you are inside of the python-class-june directory in terminal and start your conda environment]

* Create a New project
    * **django-admin startproject django-digital(this is the project name and can be anything)**
    * Start a new App inside of the project
        * **django-admin startapp products**


Once we create the files in terminal(console for windows), the file structure should look like this in atom:

    django-digital/ - We will rename this soon (src)
    manage.py
    django-digital/
        __init__.py
        settings.py
        urls.py
        wsgi.py
    products/
        __init__.py
        admin.py
        apps.py
        models.py
        test.py
        views.py

From here we can start adding things to our database through our `models.py` file (make sure you create an elephantsql database beforehand).

The following code will produce the barebones of a model that we will build on later.

```python
    class Product(models.Model):
    title = models.CharField(max_length = 50)
    description = models.CharField(max_length = 150)
    price = models.DecimalField(max_digits = 15, decimal_places = 2, default=9.99)
    sale_price = models.DecimalField(max_digits = 15, decimal_places = 2, blank=True, null=True)

    def __str__(self):
        return self.title```

To make this available in our database we need to write:
    `python manage.py makemigrations`
Then:
    `python manage.py migrate`

Now that we have a model created, we also need to create a superuser for the project and register the model to the admin panel.

We first create a superuser with this command in terminal:
    `python manage.py createsuperuser`

Next we register our model inside of the admin.py file found in products/
```python
   from .models import Product
   admin.site.register(Product)```

Now save and run the server:
    `python manage.py runserver`

Then navigate to 127.0.0.1:8000/admin

Create some products in the database and see what happens.


The remaining code will be available here. My challenge to you is to play around with the code. Clone the repo, take some things out, add some things in and see what each part of the code does. If you have questions. Bring them tomorrow.


# CRUD

Create -- add item to database -- create_view -- POST
Retrieve -- get item (s) from the database -- detail_view/list_view -- GET
Update -- Make changes/updates to the item(s) in the database -- PATCH / PUT / POST
Delete -- delete item from database -- DELETE

List -- list all items from database (or a queryset)
Search -- search items from the database
