# DRKApp Python Library

The DRKApp Python Library provides a simple interface to interact with the DRKApp API. It can be used to fetch data from different APIs based on the source (mattr, cache, or list), API type (test, staging, or production), and API endpoint (partner_list, vulnerabilities, dropdowns, or case_list).

# Getting Started

To use this library, you'll need a token to authenticate with the DRKApp API. You can get your token by contacting DRKApp support.

# Installation

You can install the library using pip:

```python
pip install drkapp
```

# Usage

First, you'll need to import the DRKApp class:

```python
from drkapp import DRKApp
```

You can then use the get_data() method to fetch data from the API:

```python
drkapp = DRKApp(token="your_token_here", api_type="test", source="mattr", api="partner_list")
```

You can then use the get_data() method to fetch data from the API:

```python
data = drkapp.get_data()
print(data)
```

# API Endpoints

The following API endpoints are available:

```json
{
  "partner_list": "users/partner-list/",
  "vulnerabilities": "case/vulnerabilities/",
  "dropdowns": "case/dropdown/",
  "case_list": "case/all-case/"
}
```

You can use the all_api_list() method to get a dictionary of all the available APIs and their endpoints.

# Documentation

DRKApp
The DRKApp class is used to interact with the DRKApp API. It requires a token to be passed in the header for authentication. It can be used to fetch data from different APIs based on the source (mattr, cache, or list), API type (test, staging, or production), and API endpoint (partner_list, vulnerabilities, dropdowns, or case_list).

`**init**(self, token=None, api_type=None, source=None, api=None)`

    Initializes a new instance of the DRKApp class with the given token, api_type, source, and api.

`all_api_list()`

    Returns a dictionary of all the available APIs and their endpoints.

`check_required_params()`

    Checks whether all the required parameters are provided.

`get_api_url()`

    returns the API URL based on the provided API type and source.

`get_data(api=None)`

    Fetches data from the API based on the provided API type and source.

`get_single_id_(api=None, id=None)`

Fetches a single record from the API by providing the record ID.

# Contributing

If you'd like to contribute to the DRKApp Python Library, please submit a pull request on GitHub.

# License

This library is licensed under the MIT License. See the LICENSE file for more information.
