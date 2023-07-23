from project import create_app

# Call the application factory function to construct a Flask application
# instance using the development configuration
if __name__ == '__main__':
    app = create_app()
    app.run()
