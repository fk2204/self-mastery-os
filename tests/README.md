# Self-Mastery OS - Test Suite

## Quick Start

```bash
# Install pytest if needed
pip install pytest pytest-cov

# Run all tests
python -m pytest tests/ -v

# Run data_manager tests only
python -m pytest tests/unit/test_data_manager.py -v

# Run with coverage report
python -m pytest tests/unit/test_data_manager.py --cov=src/data_manager --cov-report=term-missing

# Generate HTML coverage report
python -m pytest tests/unit/test_data_manager.py --cov=src/data_manager --cov-report=html
# Then open: htmlcov/index.html
```

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures (temp_dir, data_manager, freeze_time, etc.)
├── README.md                # This file
├── TEST_COVERAGE_SUMMARY.md # Detailed coverage breakdown
├── unit/
│   ├── __init__.py
│   ├── test_data_manager.py    # 60 tests - 100% coverage target
│   └── test_wisdom_engine.py   # WisdomEngine tests
├── integration/
│   └── __init__.py             # End-to-end workflow tests
└── fixtures/
    └── __init__.py             # Mock data generators
```

## Test Files

### test_data_manager.py (60 tests)
Target: 100% code coverage for `src/data_manager.py`

**Categories:**
- Initialization (4)
- JSON I/O (7)
- User Profile (6)
- Daily Logs (11)
- Weekly Reviews (3)
- Habits (15) - Critical streak logic
- Goals (3)
- Statistics (6)
- Knowledge Base (3)

**Run:**
```bash
python -m pytest tests/unit/test_data_manager.py -v
```

### test_wisdom_engine.py (66 tests)
Target: 100% code coverage for `src/wisdom_engine.py`

**Categories:**
- Initialization (5)
- Daily Wisdom Generation (4)
- Master Teaching (6)
- Daily Insight (3)
- Skill Challenge (4)
- Power Questions (2)
- Mindset Shift (2)
- Situational Advice (5)
- Module Masters (3)
- Worked Examples (4)
- Script Templates (3)
- Level Definitions (3)
- Progressive Exercises (4)
- Cross-Module Connections (2)
- Master Resources (4)
- Print Functions (6)
- Edge Cases & Error Handling (6)

**Run:**
```bash
python -m pytest tests/unit/test_wisdom_engine.py -v

# With coverage
python -m pytest tests/unit/test_wisdom_engine.py --cov=src.wisdom_engine --cov-report=term-missing

# See detailed documentation
cat tests/unit/test_wisdom_engine_summary.md
```

## Coverage Goals

| Module | Target | Tests | Status |
|--------|--------|-------|--------|
| data_manager.py | 100% | 60 | ✅ Complete |
| wisdom_engine.py | 100% | 66 | ✅ Complete |
| Overall | 80%+ | 126+ | 🔄 In Progress |

## Common Test Commands

```bash
# Run specific test by name
python -m pytest tests/unit/test_data_manager.py::test_add_habit_new -v

# Run tests matching pattern
python -m pytest tests/unit/test_data_manager.py -k "habit" -v

# Run with print statements visible
python -m pytest tests/unit/test_data_manager.py -v -s

# Stop on first failure
python -m pytest tests/unit/test_data_manager.py -x

# Show slowest tests
python -m pytest tests/unit/test_data_manager.py --durations=10

# Run failed tests from last run
python -m pytest --lf

# Run tests in parallel (requires pytest-xdist)
python -m pytest tests/unit/test_data_manager.py -n auto
```

## Writing New Tests

### Test Naming Convention
```python
def test_<function_name>_<scenario>():
    """Test <what is being tested>."""
    # Arrange
    # Act
    # Assert
```

### Using Fixtures
```python
def test_example(data_manager, sample_user_profile):
    """Test using shared fixtures."""
    # data_manager is already initialized with temp directory
    result = data_manager.save_user_profile(sample_user_profile)
    assert result is True
```

### Testing Dates
```python
def test_example_with_date(data_manager, freeze_time):
    """Test with frozen time."""
    freeze_time.set_date(datetime(2024, 1, 15, 10, 0, 0))
    # Now all datetime.now() calls return 2024-01-15 10:00:00
    log = data_manager.get_or_create_daily_log()
    assert log["date"] == "2024-01-15"
```

### Testing Errors
```python
def test_example_error(data_manager, capsys):
    """Test error handling."""
    # Trigger error condition
    result = data_manager._read_json(Path("/invalid/path"))

    # Verify result and error message
    assert result is None
    captured = capsys.readouterr()
    assert "Error reading" in captured.out
```

## Available Fixtures (conftest.py)

### Core Fixtures
- `temp_dir` - Temporary directory (auto-cleanup)
- `data_manager` - DataManager with temp dir
- `freeze_time` - Mock datetime.now()

### Sample Data
- `sample_user_profile` - User profile dict
- `sample_habit` - Habit definition dict
- `sample_daily_log` - Complete daily log
- `sample_weekly_review` - Weekly review data
- `sample_goals` - Goals structure

## Debugging Tests

```bash
# Run with Python debugger
python -m pytest tests/unit/test_data_manager.py --pdb

# Run with verbose output
python -m pytest tests/unit/test_data_manager.py -vv

# Show local variables on failure
python -m pytest tests/unit/test_data_manager.py -l

# Show all test output (not just failures)
python -m pytest tests/unit/test_data_manager.py -v -s
```

## Continuous Integration

```bash
# Run all tests with coverage (CI command)
python -m pytest tests/ --cov=src --cov-report=term-missing --cov-report=html --cov-fail-under=80
```

## Coverage Reports

After running with `--cov-report=html`, open the report:
```bash
# Windows
start htmlcov/index.html

# Mac/Linux
open htmlcov/index.html
```

## Test Quality Checklist

Before submitting tests:
- [ ] All tests pass
- [ ] Test names are descriptive
- [ ] Each test has a docstring
- [ ] Tests are independent (no shared state)
- [ ] Error paths are tested
- [ ] Edge cases are covered
- [ ] No magic numbers
- [ ] Max 30 lines per test function
- [ ] Coverage target met (80%+ overall, 100% for DataManager/WisdomEngine)

## Troubleshooting

### Import Errors
If you see "ModuleNotFoundError: No module named 'src'":
```bash
# Make sure you're in the project root
cd C:\Users\fkozi\self-mastery-os

# Verify conftest.py adds src to path
python -c "import sys; print(sys.path)"
```

### Fixture Not Found
If you see "fixture 'X' not found":
- Check conftest.py has the fixture
- Ensure conftest.py is in tests/ directory
- Verify fixture name matches exactly

### Tests Fail on Date/Time
- Use `freeze_time` fixture for deterministic dates
- Don't use datetime.now() directly in tests
- Use freeze_time.set_date() to control the "current" time

## Next Steps

1. Run coverage report to identify gaps
2. Add integration tests for workflows
3. Add tests for CLI commands
4. Set up CI/CD pipeline
5. Achieve 80%+ overall coverage
