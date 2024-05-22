# Note: this code differs from the code
# shown during the course.
# This has been added to fix problems loading dotenv
try:
    from dotenv import load_dotenv
except ImportError:
    from dotenv.main import load_dotenv

# we want this to load as soon as the globoticket package is loaded
# this makes the .env file available for the entire package
load_dotenv()
