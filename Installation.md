## Installation and Configuration Guide
1. Clone the repository.
     ```
    git clone https://github.com/D7NAMITE/ku-polls.git
    ```
2. Route into the repository.
    ```
   cd ku-polls
   ```
   After you done, the path on the terminal must appear 
similar to this:
    ```
   E:\Whatever\ku-polls>
   ```
3. Create a new virtual environment.
    ```
   python -m venv venv
   ```
4. Activate the environment.

    for Linux or MacOS
    ```
   source venv/bin/activate
   ```
   for Windows:
    ```
   call venv/Scripts/activate
   ```
5. Install the requirements from ```requirements.txt```
    ```
   pip install -r requirements.txt
   ```
6. Create the .env by copying the sample.env

    for Linux or MacOS
    ```
   cp sample.env .env
   ```
   for Windows:
    ```
   copy sample.env .env
   ```
7. Run migrations
    ```
   python manage.py migrate
   ```
8. Load fixture data
    ```
   python manage.py loaddata data/polls.json
   ```
   ,and
   ```
   python manage.py loaddata data/users.json
   ```
9. Run tests
    ```
   python manage.py test
   ```
