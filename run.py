# Archivo para ejecutar la aplicación completa
from todor import create_app

if __name__ == "__main__":
    app = create_app()
    app.run()