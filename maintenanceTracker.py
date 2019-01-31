import os

from MaintenanceTrackerAPI import create_app
from dotenv import load_dotenv

load_dotenv()

config_name = os.getenv('APP_CONFIG_NAME')  # config_name = "development"
app = create_app(config_name)

if __name__ == '__main__':
    app.run()
