1. Run: ```python manage.py runserver```
2. Create tables ```python manage.py migrate```
3. Create tables for app: ```python manage.py makemigrations xss_app```
4. Run docker: ```docker build -t wsed -f Dockerfile . && docker run -p 8000:8000 wsed```
5. Clean docker images: ```docker system prune && docker rmi wsed```