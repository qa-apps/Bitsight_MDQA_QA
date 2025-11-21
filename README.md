# BitSight MDQA QA Automation Project

## Overview
Comprehensive Playwright automation testing suite for BitSight website (https://www.bitsight.com) using Python.

## Project Structure
```
Bitsight_MDQA_QA/
├── pages/                  # Page Object Model
│   ├── base_page.py       # Base page class with common methods
│   ├── home_page.py       # Homepage page object
│   ├── products_page.py  # Products page object
│   └── home_page_real.py # Homepage with real DOM selectors
├── tests/                 # Test suites
│   ├── test_smoke_homepage.py        # Smoke tests for critical functionality
│   ├── test_navigation_links.py      # Navigation and links testing
│   ├── test_regression_full.py       # Full regression suite
│   ├── test_security_vulnerability.py # Security testing
│   ├── test_ui_elements.py           # UI element testing
│   ├── test_usability_accessibility.py # Accessibility testing
│   ├── test_page_structure.py        # Page structure validation
│   ├── test_dropdown_menus.py        # Dropdown menu testing
│   ├── test_forms_validation.py      # Form validation testing
│   ├── test_performance_metrics.py   # Performance testing
│   ├── test_cross_browser.py         # Cross-browser compatibility
│   ├── test_error_handling.py        # Error handling testing
│   ├── test_search_functionality.py  # Search functionality testing
│   ├── test_content_validation.py    # Content validation
│   ├── test_mobile_responsiveness.py # Mobile testing
│   ├── test_integration_e2e.py       # End-to-end testing
│   ├── test_data_validation.py       # Data validation testing
│   └── test_with_real_selectors.py   # Tests using actual DOM selectors
├── conftest.py           # Pytest configuration and fixtures
├── pytest.ini            # Pytest settings
├── requirements.txt      # Python dependencies
├── inspect_dom.py        # DOM inspection utility
├── extract_selectors.py  # Selector extraction utility
└── actual_selectors.json # Extracted real selectors

## Installation

### Prerequisites
- Python 3.9+
- pip package manager

### Setup
1. Clone the repository:
```bash
git clone https://github.com/qa-apps/Bitsight_MDQA_QA.git
cd Bitsight_MDQA_QA
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:
```bash
playwright install
```

## Running Tests

### Run all tests:
```bash
pytest
```

### Run specific test markers:
```bash
# Smoke tests only
pytest -m smoke

# Regression tests
pytest -m regression

# Security tests
pytest -m security

# Mobile tests
pytest -m mobile
```

### Run specific test file:
```bash
pytest tests/test_smoke_homepage.py
```

### Run with specific browser:
```bash
# Chromium only
pytest --browser chromium

# Firefox only
pytest --browser firefox

# WebKit only
pytest --browser webkit
```

### Run in headed mode:
```bash
pytest --headed
```

### Run with parallel execution:
```bash
pytest -n 4  # Run with 4 parallel workers
```

### Generate HTML report:
```bash
pytest --html=report.html --self-contained-html
```

## Test Categories

### Smoke Tests (`@pytest.mark.smoke`)
Critical functionality tests that run quickly to verify basic site operation.

### Regression Tests (`@pytest.mark.regression`)
Comprehensive tests covering all functionality to catch regressions.

### Security Tests (`@pytest.mark.security`)
Tests for vulnerabilities, XSS, SQL injection, secure headers, etc.

### Navigation Tests (`@pytest.mark.navigation`)
Tests for all navigation elements, links, and dropdowns.

### UI Tests (`@pytest.mark.ui`)
Tests for UI elements like buttons, forms, modals, etc.

### Usability Tests (`@pytest.mark.usability`)
Accessibility and usability testing including WCAG compliance.

### Performance Tests (`@pytest.mark.performance`)
Page load times, resource optimization, and performance metrics.

### Mobile Tests (`@pytest.mark.mobile`)
Mobile responsiveness and touch interaction testing.

### E2E Tests (`@pytest.mark.e2e`)
End-to-end user journey testing.

## Configuration

### Environment Variables
Create a `.env` file in the project root:
```
BASE_URL=https://www.bitsight.com
HEADLESS=False
SLOW_MO=0
TIMEOUT=30000
```

### pytest.ini Configuration
Modify `pytest.ini` to change default test settings:
- Browser selection
- Screenshot settings
- Video recording
- Parallel execution
- Test markers

## DOM Inspection Tools

### Extract Real Selectors:
```bash
python extract_selectors.py
```
This will extract actual selectors from the BitSight website and save to `actual_selectors.json`.

### Interactive DOM Inspector:
```bash
python inspect_dom.py
```
Opens Playwright Inspector for interactive DOM exploration.

## Best Practices

1. **Always inspect real DOM** before writing tests
2. **Use Page Object Model** for maintainability
3. **Keep tests independent** - each test should be able to run alone
4. **Use meaningful assertions** with clear error messages
5. **Implement proper waits** - avoid hard-coded timeouts
6. **Test data cleanup** - don't leave test data in production
7. **Cross-browser testing** - test on Chromium, Firefox, and WebKit
8. **Mobile testing** - test responsive design and touch interactions

## Project Metrics

- **Total Test Files**: 18
- **Total Page Objects**: 4
- **Test Categories**: 10
- **Lines of Code**: 150+ per test file
- **Browser Support**: Chromium, Firefox, WebKit
- **Mobile Support**: Yes
- **Accessibility Testing**: Yes
- **Security Testing**: Yes
- **Performance Testing**: Yes

## Troubleshooting

### Common Issues:

1. **Timeout errors**: Increase timeout in pytest.ini or conftest.py
2. **Element not found**: Update selectors using extract_selectors.py
3. **Browser not installed**: Run `playwright install`
4. **Permission errors**: Ensure write permissions for screenshots folder

### Debug Mode:
```bash
# Run with verbose output
pytest -v

# Run with debug output
pytest -s

# Pause on failure
pytest --pdb
```

## Contributing

1. Always update Page Objects when UI changes
2. Write tests that are resilient to minor UI changes
3. Document any new test markers in this README
4. Ensure all tests pass before committing
5. Follow the existing code style and patterns

## License
This project is for QA automation testing purposes.

## Contact
For questions or issues, please contact the QA team.

---
*Last Updated: 2023*
*Created for BitSight MDQA QA Automation*
