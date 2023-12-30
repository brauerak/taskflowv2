# TASKFLOW - TASK MANAGER APP
#### Video Demo:  https://youtu.be/IT4IcTNnrL4
#### Description:
TaskFlow is a web-based "todo" application that allows users to manage their daily tasks efficiently. The application features user registration and login, adding and deleting tasks, as well as sorting them by category.

Project Structure
The project consists of the following files:
* app.py: The main application file containing all Flask routes, user handling logic, and task management functionalities.
* models.py: Contains SQLAlchemy model definitions used to interact with the SQLite database.
* helpers.py: Helper functions like login_required decorator used to verify a logged-in user.
* requirements.txt: A list of all dependencies required to run the application.
* static/: Directory containing static files like CSS and JavaScript.
* templates/: Directory containing HTML templates used by the app to render pages.

Design Choices
Designing the application to be intuitive and easy to use was paramount. A minimalist user interface was chosen to avoid distractions and focus on the tasks at hand.

Backend
The application uses Flask and SQLite, which allows for rapid prototyping without the need for complex database setup. SQLAlchemy is used for ORM, simplifying data model management and database operations.

Frontend
Bootstrap was utilized for the frontend for its responsiveness and aesthetic appeal. Each HTML template in the templates/ directory caters to different aspects of the application, from login to task management.

Security
Security measures were a key consideration, including password hashing using Werkzeug and session management using Flask to handle user login states.

Reflections
During the project creation, I encountered several challenges, including decisions on how best to implement task sorting and managing model relationships. Ultimately, I chose to use a one-to-many relationship between users and tasks and enums for categories and priorities, proving to be effective.

Conclusion
The TaskFlow project is the culmination of many hours of coding, testing, and debugging. I am proud of the end product and believe it serves as a solid example of a task management application that can be further developed and tailored to user needs.

Future Enhancements
* Moving forward, there are several enhancements planned to make TaskFlow even more robust and user-friendly:
* Sorting by Priorities: Implementing a feature to sort tasks based on their priority levels will allow users to focus on the most critical tasks first.
* Daily Task Table Updates: A daily update feature for tasks with deadlines falling on the current day will help users stay on top of their most urgent responsibilities.
* Collaboration and Interaction with Other Users: Future versions of TaskFlow will aim to incorporate functionalities that allow users to collaborate and interact with each other. This feature will enable task sharing, group task management, and possibly a communication platform within the app for enhanced teamwork and productivity.
These enhancements are aimed at making TaskFlow not just a task manager, but a comprehensive tool for personal and collaborative productivity.

