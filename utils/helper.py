import json
import logging
import os

import requests
from typing import Optional, Dict, Any

DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def read_json_file(json_file_path: str) -> Any:
    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        raise FileNotFoundError(f"JSON file not found: {json_file_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in file {json_file_path}: {e}")


def get(url: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None):
    final_headers = headers or DEFAULT_HEADERS
    response = requests.get(url, headers=final_headers, params=params)
    return response


def post(url: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None):
    final_headers = headers or DEFAULT_HEADERS
    response = requests.post(url, json=data, headers=final_headers)
    return response


def put(url: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None):
    final_headers = headers or DEFAULT_HEADERS
    response = requests.put(url, json=data, headers=final_headers)
    return response


def delete(url: str, headers: Optional[Dict[str, str]] = None):
    final_headers = headers or DEFAULT_HEADERS
    response = requests.delete(url, headers=final_headers)
    return response


def auth_headers(token: str, base_headers: Optional[Dict[str, str]] = None):
    headers = base_headers or DEFAULT_HEADERS.copy()
    headers["Authorization"] = f"Bearer {token}"
    return headers


def validate_status(response: requests.Response, expected_status: int = 200):
    assert response.status_code == expected_status, \
        f"Expected status {expected_status}, got {response.status_code}. Response: {response.text}"


def extract_json(response: requests.Response) -> Dict[str, Any]:
    try:
        return response.json()
    except ValueError as e:
        raise AssertionError(f"Response is not valid JSON: {e}\nResponse Text: {response.text}")

def setup_logger(name: str, log_file: str = "test.log", level=logging.DEBUG) -> logging.Logger:
    os.makedirs("logs", exist_ok=True)
    log_path = os.path.join("logs", log_file)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create file handler
    file_handler = logging.FileHandler(log_path, mode='w')
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid duplicate handlers
    if not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
        logger.addHandler(file_handler)

    logger.propagate = False  # Prevent logs from being sent to root logger
    return logger

