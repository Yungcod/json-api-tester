# JSON API Tester

A simple Streamlit application that helps developers test HTTP endpoints returning JSON or validate JSON data manually.



## Features

- **Two input methods**:
  - Enter a GET API URL that returns JSON
  - Manually paste JSON content into a text area
- **JSON validation** with clear error messages
- **JSON structure analysis**:
  - Root type (object or array)
  - Number of top-level keys/items
  - Names and types of top-level keys
  - Maximum nesting depth
  - Total items count
- **JSON preview** with syntax highlighting
- **Download option** for the JSON data as a file
- **Example APIs** to test with
- **Sample JSON** data to explore

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/json-api-tester.git
cd json-api-tester
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

The application will open in your default web browser at http://localhost:8501.

### Testing an API Endpoint

1. Go to the "API URL" tab
2. Enter a valid URL that returns JSON data (or try one of the example URLs)
3. Click "Fetch and Validate"
4. View the results including JSON preview and structure analysis
5. Optionally download the JSON data as a file

### Validating Manual JSON

1. Go to the "Manual JSON" tab
2. Paste your JSON data into the text area (or use the "Load Example" button)
3. Click "Validate"
4. View the results including JSON preview and structure analysis
5. Optionally download the JSON data as a file

## Why This Tool?

JSON API Tester is useful for developers who:
- Need to quickly validate JSON responses from APIs
- Want to understand the structure of JSON data
- Need to convert and download JSON from an API endpoint
- Want to validate manually-crafted JSON before using it

## Technologies Used

- Python 3
- Streamlit - for the user interface
- Requests library - for fetching API data
- JSON standard library - for parsing and validation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE). 