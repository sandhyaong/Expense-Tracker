# Office Expense Tracker

A comprehensive Django-based web application for managing office expenses with role-based access control, approval workflows, and AI-powered insights.

## Features

### Core Functionality
- **Expense Management**: Track expenses with categories, departments, and receipt uploads
- **Role-Based Access**: Admin, Manager, and Employee roles with different permissions
- **Approval Workflow**: Submit expenses for approval with status tracking
- **Dashboard Analytics**: Visual charts showing spending patterns by category, department, and time
- **AI Insights**: Automated analysis of spending trends and patterns
- **CSV Export**: Export expense data for external analysis
- **Email Notifications**: Automated email alerts for expense approvals

### Technical Features
- **Modern UI**: Responsive design with Bootstrap styling
- **Data Visualization**: Interactive charts using Chart.js
- **File Uploads**: Receipt image storage and management
- **Database**: MySQL backend with Django ORM
- **Authentication**: Django's built-in auth system with custom profiles

## Project Structure

```
office_expense_tracker/
├── config/                 # Django project settings
│   ├── settings.py        # Main configuration
│   ├── urls.py           # Root URL configuration
│   └── wsgi.py           # WSGI application
├── expenses/              # Main expense tracking app
│   ├── models.py         # Expense, Category, Department models
│   ├── views.py          # Dashboard, CRUD operations
│   ├── urls.py           # App URL patterns
│   └── templates/        # HTML templates
├── users/                 # User management app
│   ├── models.py         # Profile model with roles
│   ├── views.py          # Authentication, user management
│   └── urls.py           # User-related URLs
├── reports/               # Future reporting features (currently empty)
├── ai_module/             # AI insights functionality
│   └── expense_ai.py     # Spending analysis logic
├── utils/                 # Utility functions
│   └── csv_exporter.py   # CSV export functionality
├── static/                # Static files (CSS, JS, images)
├── media/                 # User-uploaded files (receipts)
├── templates/             # Global templates
└── manage.py             # Django management script
```

## Installation

### Prerequisites
- Python 3.8+
- MySQL Server
- Git

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd office_expense_tracker
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirement.txt
   ```

4. **Configure MySQL Database**
   - Create a MySQL database named `office_expense_db`
   - Create a user `expense_user` with password `root123`
   - Update database settings in `config/settings.py` if needed

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open http://127.0.0.1:8000 in your browser
   - Login with the superuser credentials

## Usage

### User Roles
- **Admin**: Full access to all features, user management
- **Manager**: Can approve/reject expenses, view all reports
- **Employee**: Can submit expenses, view personal expenses

### Key Workflows

1. **Adding Expenses**
   - Navigate to "Add Expense"
   - Fill in details: title, amount, category, department
   - Upload receipt image (optional)
   - Submit for approval

2. **Approval Process**
   - Managers can view pending expenses in "Approvals"
   - Approve or reject expenses with optional comments

3. **Viewing Analytics**
   - Dashboard shows spending charts and AI insights
   - Filter by category, department, and time period

4. **Exporting Data**
   - Use the export feature to download CSV files
   - Includes all expense details for external analysis

## Configuration

### Email Settings
Update the following in `config/settings.py` for email notifications:
```python
EMAIL_HOST_USER = "your-email@gmail.com"
EMAIL_HOST_PASSWORD = "your-app-password"
```

### Database Configuration
Modify the `DATABASES` setting in `config/settings.py` for your MySQL setup:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

## API Endpoints

### Expenses App
- `GET /` - Dashboard
- `GET/POST /add-expense/` - Add new expense
- `GET /expenses/` - List all expenses
- `GET /export/` - Export expenses to CSV
- `POST /approve/<id>/` - Approve expense
- `POST /reject/<id>/` - Reject expense
- `GET /approvals/` - Pending approvals

### Categories
- `GET /categories/` - List categories
- `GET/POST /add-category/` - Add category
- `GET/POST /categories/edit/<id>/` - Edit category
- `POST /categories/delete/<id>/` - Delete category

### Departments
- `GET /departments/` - List departments
- `GET/POST /departments/add/` - Add department
- `GET/POST /departments/edit/<id>/` - Edit department
- `POST /departments/delete/<id>/` - Delete department

### Users App
- `GET/POST /login/` - User login
- `POST /logout/` - User logout
- `GET /users/` - List users
- `GET/POST /assign-role/<id>/` - Assign user role
- `GET/POST /create-user/` - Create new user

## Models

### Expense Model
- `title`: Expense title
- `amount`: Decimal amount
- `category`: Foreign key to Category
- `department`: Foreign key to Department
- `employee`: Foreign key to User
- `date`: Expense date
- `description`: Optional description
- `receipt`: Optional image upload
- `status`: Pending/Approved/Rejected
- `created_at`: Auto timestamp

### Category Model
- `name`: Category name
- `description`: Optional description

### Department Model
- `name`: Department name

### Profile Model (extends User)
- `user`: One-to-one with Django User
- `role`: Admin/Manager/Employee
- `department`: User's department

## Technologies Used

- **Backend**: Django 4.2
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Charts**: Chart.js
- **AI**: Custom Python logic for insights
- **File Handling**: Django's file upload system
- **Email**: Django's email backend with SMTP

## Development

### Running Tests
```bash
python manage.py test
```

### Code Style
- Follow Django's coding standards
- Use meaningful variable names
- Add docstrings to functions

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support or questions, please contact the development team or create an issue in the repository.