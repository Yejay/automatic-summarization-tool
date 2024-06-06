# Import the Flask module, which is needed to create a new application.
from flask import Flask

# Import the CORS module, which allows Cross-Origin Resource Sharing.
from flask_cors import CORS

# Define a function to create a new Flask application.
def create_app():
    # Create a new Flask application instance.
    app = Flask(__name__)
    
    # Enable CORS for the application. This allows the server to specify who can access the resources.
    CORS(app)

    # The `with app.app_context():` statement is used to manage the application context.
    # The application context keeps track of the application-level data during a request, CLI command, or other activity.
    with app.app_context():
        # Import the function to register routes from the routes module.
        from .routes import register_routes
        
        # Register the routes with the Flask application instance.
        register_routes(app)

    # Return the Flask application instance.
    return app