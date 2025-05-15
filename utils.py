import json
import requests
from typing import Dict, List, Tuple, Any, Union, Optional

def fetch_json_from_url(url: str) -> Tuple[bool, Union[Dict, List, str]]:
    """Fetch JSON data from a URL."""
    try:
        # Add headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Check if the content type is JSON
        content_type = response.headers.get('Content-Type', '')
        if 'application/json' not in content_type and 'text/javascript' not in content_type:
            # Try to parse anyway, but warn the user
            parsed_data = response.json()
            return True, parsed_data
        
        return True, response.json()
    except requests.exceptions.Timeout:
        return False, "Request timed out. The server took too long to respond."
    except requests.exceptions.ConnectionError:
        return False, "Connection error. Please check your internet connection and the URL."
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if hasattr(e, 'response') else 'unknown'
        return False, f"HTTP Error {status_code}: The server returned an error. Please check the URL."
    except requests.exceptions.RequestException as e:
        return False, f"Error fetching data: {str(e)}"
    except json.JSONDecodeError:
        return False, "Invalid JSON response from the URL. The URL might not return valid JSON data."
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

def validate_json_string(json_str: str) -> Tuple[bool, Union[Dict, List, str]]:
    """Validate a JSON string and return the parsed data if valid."""
    if not json_str or json_str.strip() == '':
        return False, "Empty input. Please enter some JSON data."
        
    try:
        parsed_data = json.loads(json_str)
        return True, parsed_data
    except json.JSONDecodeError as e:
        line_col = f" at line {e.lineno}, column {e.colno}"
        error_msg = f"Invalid JSON: {e.msg}{line_col}"
        return False, error_msg
    except Exception as e:
        return False, f"Error parsing JSON: {str(e)}"

def get_data_type(value: Any) -> str:
    """Get the data type of a value in a more readable format."""
    if isinstance(value, dict):
        return "object"
    elif isinstance(value, list):
        if len(value) > 0:
            # Check if all items are of the same type
            item_types = set(get_data_type(item) for item in value)
            if len(item_types) == 1:
                return f"array of {next(iter(item_types))}"
            return "array (mixed types)"
        return "array (empty)"
    elif isinstance(value, str):
        return "string"
    elif isinstance(value, int):
        return "integer"
    elif isinstance(value, float):
        return "number"
    elif isinstance(value, bool):
        return "boolean"
    elif value is None:
        return "null"
    else:
        return type(value).__name__

def calculate_nesting_depth(data: Union[Dict, List]) -> int:
    """Calculate the maximum nesting depth of a JSON structure."""
    if isinstance(data, dict):
        if not data:
            return 1
        return 1 + max((calculate_nesting_depth(v) for v in data.values() if isinstance(v, (dict, list))), default=0)
    elif isinstance(data, list):
        if not data:
            return 1
        return 1 + max((calculate_nesting_depth(item) for item in data if isinstance(item, (dict, list))), default=0)
    else:
        return 0

def count_items_recursively(data: Union[Dict, List]) -> int:
    """Count the total number of items in the JSON structure recursively."""
    if isinstance(data, dict):
        return len(data) + sum(count_items_recursively(v) for v in data.values() if isinstance(v, (dict, list)))
    elif isinstance(data, list):
        return len(data) + sum(count_items_recursively(item) for item in data if isinstance(item, (dict, list)))
    else:
        return 0

def analyze_json_structure(data: Union[Dict, List]) -> Dict:
    """Analyze the structure of JSON data and return summary information."""
    root_type = get_data_type(data)
    
    # Handle top-level keys for objects
    top_level_keys = {}
    if isinstance(data, dict):
        top_level_count = len(data)
        for key, value in data.items():
            top_level_keys[key] = get_data_type(value)
    elif isinstance(data, list):
        top_level_count = len(data)
        if top_level_count > 0:
            # Sample the first item for array types
            first_item_type = get_data_type(data[0])
            top_level_keys = {"(array items)": first_item_type}
            
            # If it's an array of objects, show the keys of the first object
            if first_item_type.startswith("object") and isinstance(data[0], dict):
                for key, value in data[0].items():
                    top_level_keys[f"[0].{key}"] = get_data_type(value)
        else:
            top_level_keys = {"(array items)": "empty"}
    else:
        top_level_count = 0
    
    # Calculate nesting depth
    depth = calculate_nesting_depth(data)
    
    # Count total items
    total_items = count_items_recursively(data)
    
    return {
        "root_type": root_type,
        "top_level_count": top_level_count,
        "top_level_keys": top_level_keys,
        "nesting_depth": depth,
        "total_items": total_items
    } 