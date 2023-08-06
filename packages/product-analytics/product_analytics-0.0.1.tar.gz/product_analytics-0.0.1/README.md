# Product Analytics

`peak_ai.product_analytics`` is a Python wrapper for the Segment API, designed to provide an easy way to track and manage analytics in your Python applications.

The library provides the following key features:

- Initialization with a Segment write key and an enabled flag
- Identify a user
- Track a page view
- Track a custom event
- Reset the state

## Installation

To use this library, you can install it directly from pip:

```bash
pip install peak_ai.product_analytics
```

## Usage

### Initialization

First, initialize the Segment client:

```python
import analytics

analytics.init({
  "write_key": "YOUR_SEGMENT_WRITE_KEY",
  "enabled": True # You can optionally set to false, for example in a non-production environment using the env variable
})
```

### Identifying a User

To identify a user, provide a dictionary containing their ID, email, tenant, and session ID:

```python
analytics.identify({
  "id": "user123",
  "email": "user123@example.com",
  "tenant": "tenant1",
  "session_id": "session123"
})
```

### Tracking a Page View

To track a page view, provide the path as part of a dictionary:

```python
analytics.page({
  "path": "/home"
})
```

### Tracking an Event

To track a custom event, provide a dictionary containing the event name and optionally, an additional properties dictionary:

```python
analytics.track({
  "name": "User Signed Up",
  "properties": {
    "plan": "Pro"
  }
})
```

### Resetting the State

To reset the state (e.g., when a user logs out), simply call the reset function:

```python
analytics.reset()
```

## Developer Quick Start

If you want to contribute to the development of this package, here are the steps to get started:

1. Clone the repository:

```bash
git clone https://github.com/peak-platform/product-analytics-py.git
cd product-analytics-py
```

2. Install the development and package dependencies:

```bash
pip install ".[dev]"
```

3. Set up pre-commit hooks:

```bash
pre-commit install
```

4. Run the tests:

```bash
pytest
```

**You're good to go!**

## Running Tests

We use Pytest for our tests. To run tests, use the pytest command from the root directory of the project:

```bash
pytest
```

## Linting

We use Black for our code formatting. To format your code, run:

```bash
black .
```

This will format your Python files in place according to the Black code style.

## Contributing

Contributions are welcome. Please make a pull request.

## License

This project is licensed under the terms of the MIT license.
