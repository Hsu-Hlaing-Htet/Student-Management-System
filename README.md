
# Student Management System
#### Video Demo: https://youtu.be/SGLG6QBsbc4?si=6k0yyPO2SycbDe0b 
#### Description: This web-based Student Management System is designed to help schools manage their students, teachers, courses, sections, and payments efficiently. It provides an intuitive dashboard for tracking student and teacher data, along with tools for managing sections, courses, and payrolls.

## Table of Contents
- [Features](#features)
  - [User Management](#user-management)
  - [Dashboards](#dashboards)
  - [Student Management](#student-management)
  - [Teacher Management](#teacher-management)
  - [Course Management](#course-management)
  - [Section Management](#section-management)
  - [Payment Management](#payment-management)
- [Technology Stack](#technology-stack)
- [Setup Instructions](#setup-instructions)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [License](#license)
- [Contributing](#contributing)
- [Contact](#contact)

## Features

### User Management
- **Signup/Login**: Secure user authentication with password hashing.
- **Reset Password**: Placeholder for email-based password recovery.
- **Session Management**: Automatic redirects for logged-in users.

### Dashboards
- Overview of total counts for:
  - Students
  - Teachers
  - Courses
  - Sections
  - Payments
- Quick access to data insights.

### Student Management
- Add, edit, delete, and view student records.
- Associate students with specific courses and sections.
- Filter student information for better management.

### Teacher Management
- Add, edit, delete, and view teacher profiles.
- Specializations and courses assigned for detailed records.

### Course Management
- Create, edit, delete, and list courses.
- Configure course schedules, fees, and descriptions.

### Section Management
- Add, edit, delete, and view sections.
- Room names and sections assigned for detailed records.

### Payment Management
- Create, edit, delete, and list payments.
- Configure payment dates, fees, and manage student payments for sections.

## Technology Stack
- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript (with optional frameworks)
- **Authentication**: Flask-Session, Werkzeug for password hashing
- **Version Control**: Git, GitHub

## Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/username/repository.git
   cd repository


2. Set up the Python virtual environment:

   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Run the Flask development server:
   ```
   pip install -r requirements.txt
   ```

5. Access the application:
   ```
   Visit http://127.0.0.1:5000/ in your web browser.
   ```
### Project Structure
```
Student-Management-System/
│
├── app/                    # Application code
│   ├── templates/          # HTML templates
│   ├── static/             # CSS, JavaScript files
├── app.py                  # Main file
├── config.py               # Configuration file
├── helpers.py              # Helper file
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── ...
```
## Usage

### Managing Student Data
- Add, view, update, or delete student records.
- Filter students by course, section, or other criteria.

### Managing Teachers
- Manage teacher profiles and assign them to courses and sections.

### Managing Courses and Sections
- Create, update, and delete courses.
- Manage sections and assign students to them.

### Payment Management
- Track and manage payments for students.
- Generate reports for payments and fees.

### Authentication and User Management
- Sign up and log in as an admin.
- Manage user roles and permissions for different types of users (e.g., Admin, Teacher).

## License
This project is licensed under the MIT License.

## Contributing
Contributions are welcome! If you would like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new feature branch (e.g., `git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## Contact
For any inquiries or support, feel free to reach out:

- Email: hsuhtet562@gmail.com
- GitHub: https://github.com/Hsu-Hlaing-Htet

