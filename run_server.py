import os
from dotenv import load_dotenv
from subprocess import run

# Load environment variables from .env file
load_dotenv()

# Run the OpenAlgo server module
run(["python", "openalgo_server_module.py"])
