# eCommerce Marketplace Application

## Project Overview

This project is a Django eCommerce Marketplace application that uses
MariaDB as the relational database backend.

Users can register as either buyers or vendors. Vendors can create stores
and manage products. Buyers can browse products, add products to a cart,
checkout, view orders, and submit product reviews.

## Features

- Buyer and vendor registration
- Login, logout, and password reset
- Role-based dashboard links
- Vendor-only store management
- Vendor-only product management
- Buyer shopping cart
- Checkout and order history
- Product reviews
- MariaDB database backend
- Planning folder with required planning documents

## Project Structure

```text
ecommerce_marketplace/
├── manage.py
├── requirements.txt
├── README.md
├── planning/
├── ecommerce_marketplace/
└── marketplace/
```

## Setup Instructions

### Step 1: Get the Project Folder

Download, extract, or clone the project folder onto your computer.

### Step 2: Enter the Main Project Folder

Open a terminal in the folder that contains `manage.py` and
`requirements.txt`.

```bash
cd ecommerce_marketplace
```

### Step 3: Create the Virtual Environment

Create the virtual environment inside the project folder.

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux or macOS:

```bash
source venv/bin/activate
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Create the MariaDB Database

Log into MariaDB and run:

```sql
CREATE DATABASE ecommerce_marketplace;

CREATE USER 'marketplace_user'
IDENTIFIED BY 'password123';

GRANT ALL PRIVILEGES
ON ecommerce_marketplace.*
TO 'marketplace_user';

FLUSH PRIVILEGES;
```

### Step 7: Confirm the Database Settings

Open `ecommerce_marketplace/settings.py` and confirm that the database
credentials match your MariaDB database.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecommerce_marketplace',
        'USER': 'marketplace_user',
        'PASSWORD': 'password123',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Step 8: Check the Project

```bash
python manage.py check
```

### Step 9: Apply Migrations

The initial migration file is included in the project.

```bash
python manage.py migrate
```

If you change the models, run this first:

```bash
python manage.py makemigrations
```

### Step 10: Create an Admin User

```bash
python manage.py createsuperuser
```

### Step 11: Run the Development Server

```bash
python manage.py runserver
```

Open the application at:

```text
http://127.0.0.1:8000/
```

## Testing

```bash
python manage.py test
```

## Important Notes

- The project uses MariaDB, not SQLite.
- The MariaDB database must exist before running migrations.
- The `venv` folder should be created inside the project folder but should
  not be submitted as source code.
- Role-based permissions are enforced in views and templates.
- The `ReviewForm` class is included in `marketplace/forms.py`.
- The `Review` model is included in `marketplace/models.py`.
