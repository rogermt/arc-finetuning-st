import subprocess
import requests
import time
import os
import logging
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

logging.basicConfig(level=logging.INFO)

LITELLM_DEFAULT_FILE = "config.yaml"
LITELLM_PROXY_TIMEOUT = int(os.environ.get('LITELLM_PROXY_TIMEOUT'))
LITELLM_CONFIG_FILE=os.environ.get('LITELLM_CONFIG_FILE')

def is_litellm_running() -> bool:
    health_check_url = 'http://localhost:4000/health/liveliness'
    try:
        response = requests.get(health_check_url, headers={'accept': 'application/json'})
        return response.status_code == 200
    except requests.ConnectionError:
        return False

def wait_for_server_to_start(timeout: int=LITELLM_PROXY_TIMEOUT) -> bool:
    start_time = time.time()
    while time.time() - start_time < timeout:
        if is_litellm_running():
            return True
        time.sleep(1)
    return False

def start_litellm_proxy(config_file: Optional[str] = LITELLM_DEFAULT_FILE):
    try:
        subprocess.Popen(["litellm", "--config", config_file])
    except Exception as e:
        logging.error(f"Error starting LiteLLM proxy server: {e} using config file: {config_file}")  
        return False
    return True

def start() -> None:
    server_started = False
    if not is_litellm_running():
        if start_litellm_proxy(LITELLM_CONFIG_FILE):
            server_started = wait_for_server_to_start()
        else:
            server_started = False
    else:
        server_started = True

    if not server_started:
        logging.error("Failed to start LiteLLM proxy server within the timeout period.")
    else:
        logging.info("LiteLLM proxy server started successfully.")