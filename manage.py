import os
import sys
from manager import create_app
from config.settings import DevConfig

def run():
    """Run administrative tasks."""
    app = create_app()
    app.run()

if __name__ == '__main__':
    run()