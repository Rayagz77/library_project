📚 Library Project
Library Project is a web application developed with Flask for managing books, authors, and categories. It also integrates advanced features such as AI using Hugging Face and adheres to best development practices.

User Experience:
Users can browse available books.
Users can add books to their cart to prepare an order.
To complete an order, users must:
Log in to their account.
Create an account if not already registered.
Admin Features:
CRUD (Create, Read, Update, Delete):
Books Management: Add, edit, delete, and view books.
Authors Management: Add, edit, delete, and view authors.
Categories Management: Add, edit, delete, and view categories.
Architecture and Technologies:
Backend Framework: Flask (Python).
Database: SQLAlchemy (ORM).
Front-End: HTML, CSS (Responsive Design).
AI: Integration of a Hugging Face model.
Development Practices:
Use of pytest for testing.
Adherence to coding standards with Flake8 and Black.
Typing with typing.
Extras:
Compliance with GDPR standards.
Zoning, wireframes, and mockups designed with Figma.
Project planning and tracking with Kanban.
🛠️ Installation and Configuration
Prerequisites:
Python 3.10 or higher.
SQLite (default database in SQLAlchemy).
git installed.
Installation Steps:
Clone the project:


git clone https://github.com/your_username/library_project.git
cd library_project
Create and activate a virtual environment:

bash
Copier le code
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
Install dependencies:

bash
Copier le code
pip install -r requirements.txt
Set up the database:

bash
Copier le code
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
Run the application:

bash
Copier le code
flask run
🚀 Features to Explore
User Dashboard: Browse books and manage orders.
Admin Dashboard: Manage books, authors, and categories.
AI Features: Personalize content with Hugging Face integration.
🤝 Contributions
Feel free to fork the repository and submit pull requests for enhancements or fixes. Contributions are welcome!

📄 License
This project is licensed under the MIT License.

