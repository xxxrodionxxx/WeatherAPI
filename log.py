import logging

# Logger setup
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log',
    filemode='a'
)

# Creating a logger
logger = logging.getLogger(__name__)
