# Building a REST API with Python 3
> This is my version of [this repo](https://github.com/codesensei-courses/python_3_rest_api). This includes comments
> and changes that I did during this project

Demo code for the course "Building a REST API with Python 3" on [Pluralsight](https://app.pluralsight.com/library/courses/python-3-building-rest-api/table-of-content).

There's a commit for each module in the course, as well as a tag:
- [Module 2: Getting Started](https://github.com/codesensei-courses/python_3_rest_api/releases/tag/project-start)
- [Module 3: Creating a datamodel](https://github.com/codesensei-courses/python_3_rest_api/releases/tag/datamodel-start)
- [Module 3 (end): Created database models, added .env](https://github.com/codesensei-courses/python_3_rest_api/releases/tag/datamodel-end)
- [Module 4 (end): Api endpoints and unit tests](https://github.com/codesensei-courses/python_3_rest_api/releases/tag/api-end)
- [Module 5: Exercise: Reading Content from the Filesystem](https://github.com/codesensei-courses/python_3_rest_api/releases/tag/files-start)
- [Module 5: Exercise: Parsing Frontmatter](https://github.com/codesensei-courses/python_3_rest_api/releases/tag/files-parse)
- [Module 5 (end): Fixed the final unit test](https://github.com/codesensei-courses/python_3_rest_api/releases/tag/course-end)

# TODOs
- Build APIs to add events and categories

# Links and References
- [SQLAlchemy - PostgreSQL setup for psycopg2](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg2)
- [SQLAlchemy - PostgreSQL documentation](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#dialect-postgresql)
- [codesensei course - python3 rest api demo repo](https://github.com/codesensei-courses/python_3_rest_api)
- [FastAPI documentation](https://fastapi.tiangolo.com/)
- 

# Database
Database is currently a PostgreSQL database called _events.db_. I already created the tables in events.db using [this file](https://raw.githubusercontent.com/codesensei-courses/python_3_rest_api/bb66db9a57b8c2281f62d20cb9cb5c952427cc87/database.ddl)

# Setup instructions

## 1. Install poetry

Follow the instructions at https://python-poetry.org/docs/#installation

## 2. Clone this repository

Check out any specific commit you like.

## 3. Install dependencies

Inside the project, run `poetry install`.

## 4. Run the project

The command for this is `poetry run python runserver.py`.

You can now view the project at http://localhost:8000
Docs can be found at [http://localhost:8000/docs](http://localhost:8000/docs)

## 5. Test the project

For this you run `poetry run pytest`.
