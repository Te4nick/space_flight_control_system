# Space Flight Control System
## Development
- Clone repo:
  ```bash
  git clone <link>
  ```
- cd to cloned project:
  ```bash
  cd space_flight_control_system
  ```
- Set up virtual environment:
  ```bash
  python -m venv .venv
  ```
- Activate virtual environment:
  ```bash
  .\venv\Scripts\activate
  ```
- Install project:
  ```bash
  pip install .
  ```
- Run django development server:
  ```bash
  python manage.py runserver
  ```
- Run all tests:
  ```bash
  python manage.py test
  ```
- Run unit tests:
  ```bash
  python manage.py test flight/tests/unit_tests
  ```
- Run component tests:
  ```bash
  python manage.py test flight/tests/component_tests
  ```
