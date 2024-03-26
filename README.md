# Welcome to WSED
WSED (Web Security Exploits and Defences) is a tool designed primarily for Computer Security students of The University of Edinburgh, who have just learned about the web security theory, but have very little to no practical experience with web security exploits and defences. However, apart from concepts taught in the Computer Security course, this tool assumes basic knowledge of JavaScript and HTML.

## How to use
This web application runs locally as a Docker container and serves both as the source of information and assignments, and as the target vulnerable application you as the user will exploit. The first tutorial focused on XSS mimics an application for creating, browsing and searching blogs. You can also register and log in with different user accounts, but this is not necessary unless you attempt the advanced XSS exercises (coming soon!).

## Run for the first time
1. Clone the repository to your machine
2. Download and install [Docker](https://www.docker.com/get-started/)
3. Once it is installed, be sure it is running. You do not have to do anything else with it
4. Navigate to the project's root directory
5. Checkout the beta branch: ```git checkout beta```
6. Build and run using Docker: ```docker build -t wsed -f Dockerfile . && docker run -p 8000:8000 wsed```
7. Now the application is running, and you can access it on the address outputted in your terminal

### Other useful commands for Django
These commands may be useful if you decide to contribute to this project and run Django on your machine.
1. Run application: ```python manage.py runserver```
2. Create/update all tables ```python manage.py migrate```
3. Create/update changes to tables for specific app: ```python manage.py makemigrations xss_app```
