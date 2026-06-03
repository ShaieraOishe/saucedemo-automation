# SauceDemo Automation Test Suite

Automated end-to-end tests for [SauceDemo](https://www.saucedemo.com/) covering three assessment scenarios using Python, Playwright, pytest, and Allure.

---

## Test Scenarios

| # | Marks | User | Description |
|---|---|---|---|
| Q1 | 20 | `locked_out_user` | Attempt login and verify the error message |
| Q2 | 50 | `standard_user` | Reset state → add 3 items → verify checkout names & total → finish order → reset & logout |
| Q3 | 30 | `performance_glitch_user` | Reset state → sort Z→A → add first item → verify checkout → finish order → reset & logout |

---

## Tech Stack

| Tool | Version | Purpose |
|---|---|---|
| **Python** | 3.10+ | Programming language |
| **Playwright** | 1.49.1 | Browser automation (Chromium) |
| **pytest** | 8.3.4 | Test runner & assertions |
| **allure-pytest** | 2.13.5 | Allure report integration |
| **Allure CLI** | Latest | HTML report generation |
| **pytest-timeout** | 2.3.1 | Timeout handling for slow users |

---

## Project Structure

```
saucedemo-automation/
├── pages/                                  # Page Object Model classes
│   ├── __init__.py
│   ├── login_page.py                       # Login page interactions
│   ├── inventory_page.py                   # Products page + hamburger menu
│   ├── cart_page.py                        # Cart page interactions
│   └── checkout_page.py                    # Checkout info, overview & confirmation
│
├── tests/                                  # Test scenarios
│   ├── __init__.py
│   ├── test_q1_locked_out_user.py          # Q1 [20 marks]
│   ├── test_q2_standard_user.py            # Q2 [50 marks]
│   └── test_q3_performance_glitch_user.py  # Q3 [30 marks]
│
├── conftest.py                             # Shared fixtures (browser, password)
├── pytest.ini                              # pytest + Allure configuration
├── requirements.txt                        # Python dependencies
├── Makefile                                # make targets
├── run_tests.sh                            # Shell script runner
├── allure-results/                         # Raw Allure data (auto-generated)
├── allure-report/                          # HTML report output (auto-generated)
└── .gitignore
```

---

## Prerequisites

### 1. Python 3.10 or higher
```bash
python3 --version
```

### 2. Allure CLI

**macOS:**
```bash
brew install allure
allure --version
```

**Windows (Scoop):**
```bash
scoop install allure
```

**Linux:**
```bash
sudo apt-get install -y allure
```

---

## Setup & Installation

```bash
# 1. Clone the repository
git clone https://github.com/shaierasultanaoishe/saucedemo-automation.git
cd saucedemo-automation

# 2. Create a virtual environment
python3 -m venv .venv

# 3. Activate the virtual environment
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

# 4. Install Python dependencies
pip install -r requirements.txt

# 5. Install Playwright Chromium browser
playwright install chromium
```

> **Important:** Steps 3–5 must be repeated every time you open a new terminal window.
> Always activate the venv with `source .venv/bin/activate` before running any tests.

---

## Running Tests

### Option A — Shell Script (Recommended)

Make the script executable once:
```bash
chmod +x run_tests.sh
```

| Command | What it runs |
|---|---|
| `./run_tests.sh` | All tests sequentially (Q1 → Q2 → Q3) + Allure report |
| `./run_tests.sh q1` | Q1 only + Allure report |
| `./run_tests.sh q2` | Q2 only + Allure report |
| `./run_tests.sh q3` | Q3 only + Allure report |
| `./run_tests.sh report` | Generate & open Allure report only (no tests) |

---

### Option B — pytest directly

```bash
# Activate venv first
source .venv/bin/activate

# Run Q1 only
pytest tests/test_q1_locked_out_user.py -v

# Run Q2 only
pytest tests/test_q2_standard_user.py -v

# Run Q3 only
pytest tests/test_q3_performance_glitch_user.py -v

# Run ALL three sequentially
pytest tests/test_q1_locked_out_user.py \
       tests/test_q2_standard_user.py \
       tests/test_q3_performance_glitch_user.py -v
```

After running, generate and open the Allure report:
```bash
allure generate allure-results --clean -o allure-report
allure open allure-report
```

---

### Option C — Makefile

| Command | What it runs |
|---|---|
| `make install` | Create venv + install deps + Playwright |
| `make test-q1` | Q1 only + Allure report |
| `make test-q2` | Q2 only + Allure report |
| `make test-q3` | Q3 only + Allure report |
| `make test-all` | All tests sequentially + Allure report |
| `make report` | Generate & open Allure report only |
| `make clean` | Remove allure-results, allure-report, cache |

---

## Allure Report

Every test run automatically writes results to `allure-results/`. The HTML report is generated at `allure-report/index.html` and opens in your browser.

The report includes:
- ✅ Pass / fail status per test
- 📸 Full-page screenshot on test completion
- 🎥 Video recording of each test
- 📝 Step-by-step execution log
- 💰 Price breakdown attachments (Q2, Q3)
- 🏷️ Product name verification attachments (Q2, Q3)

---

## Credentials Reference

| Username | Password | Notes |
|---|---|---|
| `locked_out_user` | `secret_sauce` | Blocked — cannot log in |
| `standard_user` | `secret_sauce` | Normal user |
| `performance_glitch_user` | `secret_sauce` | Slow responses by design |

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `zsh: command not found: pip` | Use `pip3` or `python3 -m pip` |
| `externally-managed-environment` error | Create and activate a venv first (see Setup) |
| `zsh: permission denied: ./run_tests.sh` | Run `chmod +x run_tests.sh` first |
| `allure: command not found` | Run `brew install allure` |
| `No module named playwright` | Activate your venv, then run `pip install -r requirements.txt` |
| Tests timeout on Q3 | `performance_glitch_user` is intentionally slow — timeout is set to 60s |
| `ModuleNotFoundError: pages` | Run pytest from the project root directory, not from inside `tests/` |
| Port conflict on `allure open` | Use `allure open allure-report -p 9999` |
  <img width="1351" height="757" alt="Screenshot 2026-06-03 at 12 41 00 PM" src="https://github.com/user-attachments/assets/e1616c07-ca4c-400b-baa2-de5a67454e42" />
