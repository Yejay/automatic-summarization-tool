# Import the create_app function from the app module.
# The create_app function is a factory function that creates a new Flask application instance.
from app import create_app

# Call the create_app function to create a new Flask application instance.
# The create_app function configures and returns a new Flask application.
app = create_app()

# Check if this script is the entry point of the program.
# The __name__ variable is a special variable in Python. When a script is the entry point of the program, __name__ is set to "__main__".
if __name__ == '__main__':
    # Start the Flask development server.
    # The run method starts the Flask development server at http://127.0.0.1:5000/ (by default).
    # The debug=True option enables debug mode. This provides more detailed error messages, and it allows the server to reload itself whenever code changes are detected.
    app.run(debug=True)