# CoachCode Backend Project with Flask

This project serves as **my thesis project for my university degree**.  CoachCode addresses a crucial issue in the landscape of competitive IT interviews, providing a comprehensive suite of functionalities designed to empower users throughout their job search and interview preparation process. The application offers a range of features aimed at enhancing technical skills, interview performance, and preparation for a successful career. This project is built using Flask and includes multiple modules for managing various functionalities.  

## **Documentation**
[Licenta_Final.pdf](https://github.com/user-attachments/files/16427196/Licenta_Final.pdf)

## **Presentation**
[prezentare.pdf](https://github.com/user-attachments/files/16427217/prezentare.pdf)

## **Demo**
https://www.youtube.com/watch?v=yQLhxI329-s


## Main Modules

### 1. Auth

The `auth` module is responsible for managing user authentication and authorization. It includes features for registration, login, password reset, and session management.

### 2. Chatbot

The `chatbot` module provides functionalities for user-to-user chat and automated interactions based on artificial intelligence for support or frequently asked questions.

### 3. Coding Practice

The `codingpractice` module facilitates coding practice, offering users exercises, questions, or projects to improve their programming skills.

### 4. Community

The `community` module allows users to interact and collaborate within a community. It includes features like forums, discussion groups, and resource sharing.

### 5. CV Maker

The `cvmaker` module enables users to create and manage personalized resumes. It includes features for uploading images, editing text, and exporting in various formats.

### 6. Notification

The `notification` module manages user notifications. It includes functionalities for sending and managing notifications related to user activities or app updates.

### 7. Problem Submissions

The `problemsubmissions` module allows users to submit and manage technical problems or questions. It includes features for evaluation, feedback, and progress tracking.

### 8. Profile User

The `profileuser` module facilitates the management of user profiles. It includes features for uploading and managing profile information, including photos and personal descriptions.

## Deployment

To deploy the Flask application, follow these steps:

1. **Install Dependencies**: Ensure all dependencies are installed. You can install the dependencies listed in `requirements.txt` using `pip install -r requirements.txt`.
   
2. **Configuration**: Check and update the `config.py` file with the appropriate settings for the deployment environment (e.g., database settings, secret keys, etc.).

3. **Setup and Launch**: Set the environment variable `FLASK_APP` to indicate the main application file (usually `run.py` or `app/__init__.py`) and then start the Flask server.

    ```bash
    export FLASK_APP=run.py
    flask run
    ```

    Or, if using `python -m flask`:

    ```bash
    python -m flask run
    ```

4. **Access the Application**: Access the application in a browser at `http://localhost:5000` or the address specified by the Flask server.
