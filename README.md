
# More detailed instructions to come...

# Required tools
- Python3
- pip3
- Postgres

# Installing Dependencies
- python -m venv venv (create a virtual env folder called venv)
- pip3 install -r requirements.txt (install all of the dependencies in the requirements.txt into venv)

# Updating dependencies
- If you add a new dependency to the project, you should add it to the requirements.txt

## Make sure you are working from inside a virtual env to ensure flask commands run properly:

# Setting up your environment variables
- You should have a file in the root directory called .env with the following variables set:
    FLASK_APP=app
    FLASK_ENV=development

# Running Flask application
- flask run (this only works if you have your environment variables defined as described in the previous step above)

# Running Migrations to set up DB
- If you update a model (in app/models.py), you need to create a new migration version by running the following command:
    flask db migrate -m 'INSERT MESSAGE HERE, e.g. Delete token column from users table'
- The above command will automatically generate a new migration file in migrations/versions. You should manually check this file to ensure that the generated code is actually what you want.
- You can then run the upgrade command to actually carry out the changes described in the migration file, and update your DB schema:
    flask db upgrade
- When pulling down changes from Github, if you see there is a new migration file, run the upgrade command to ensure that your schema is up to date

# Recommendation system
Input a choosed accommodation ID and it could return the recommended accommodation ID based on similarity matrix







