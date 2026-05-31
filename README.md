# SauceDemo Automation Test Suite

Automated end-to-end tests for [SauceDemo](https://www.saucedemo.com/) covering three assessment scenarios.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| **Python 3.10+** | Programming language |
| **Playwright** | Browser automation |
| **pytest** | Test runner & assertions |
| **allure-pytest** | Allure report integration |
| **Allure CLI** | HTML report generation |

---

## Project Structure

```
saucedemo-automation/
├── pages/                            # Page Object Model classes
│   ├── __init__.py
│   ├── login_page.py                 # Login page interactions
│   ├── inventory_page.py             # Products/inventory + hamburger menu
│   ├── cart_page.py                  # Cart page interactions
│   └── checkout_page.py             # Checkout info, overview & confirmation
│
├── tests/                            # Test scenarios
│   ├── __init__.py
│   ├── test_q1_locked_out_user.py    # Q1 [20 marks] – locked_out_user error
│   ├── test_q2_standard_user.py      # Q2 [50 marks] – standard_user journey
│   └── test_q3_performance_glitch_user.py  # Q3 [30 marks] – glitch user journey
│
├── allure-results/                   # Raw Allure data (auto-generated)
├── allure-report/                    # HTML report output (auto-generated)
├── conftest.py                       # Shared pytest fixtures (browser, URL, password)
├── pytest.ini                        # Pytest + Allure configuration
├── requirements.txt                  # Python dependencies
├── Makefile                          # Convenience make targets
├── run_tests.sh                      # Shell script runner
└── .gitignore
```

---

## Prerequisites

### 1. Python 3.10 or higher
```bash
python3 --version    # should be 3.10+
```

### 2. Allure CLI (for HTML reports)

**macOS (Homebrew):**
```bash
brew install allure
```

**Windows (Scoop):**
```bash
scoop install allure
```

**Linux:**
```bash
sudo apt-get install -y allure
# OR use the official installer:
# https://docs.qameta.io/allure/#_installing_a_commandline
```

Verify installation:
```bash
allure --version
```

---

## Setup & Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/saucedemo-automation.git
cd saucedemo-automation

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install Playwright browser (Chromium)
playwright install chromium
```

---

## Running Tests

### Option A — Using the Shell Script

Make the script executable first (one-time):
```bash
chmod +x run_tests.sh
```

| Command | What it runs |
|---|---|
| `./run_tests.sh` | All tests sequentially (Q1 → Q2 → Q3) |
| `./run_tests.sh q1` | Q1 only |
| `./run_tests.sh q2` | Q2 only |
| `./run_tests.sh q3` | Q3 only |
| `./run_tests.sh report` | Generate & open Allure report (no tests) |

Each run **automatically generates and opens** the Allure HTML report.

---

### Option B — Using Make

| Command | What it runs |
|---|---|
| `make install` | Create venv + install deps + Playwright |
| `make test-q1` | Q1 only + report |
| `make test-q2` | Q2 only + report |
| `make test-q3` | Q3 only + report |
| `make test-all` | All tests sequentially + report |
| `make report` | Generate & open report (no tests) |
| `make clean` | Remove generated artifacts |

---

### Option C — Using pytest directly

```bash
# Activate venv first
source .venv/bin/activate

# Run Q1 only
pytest tests/test_q1_locked_out_user.py -v

# Run Q2 only
pytest tests/test_q2_standard_user.py -v

# Run Q3 only
pytest tests/test_q3_performance_glitch_user.py -v

# Run ALL three tests sequentially
pytest tests/test_q1_locked_out_user.py \
       tests/test_q2_standard_user.py \
       tests/test_q3_performance_glitch_user.py -v

# After running, generate the Allure report manually:
allure generate allure-results --clean -o allure-report
allure open allure-report
```

> **Note:** `pytest.ini` is pre-configured with `--alluredir=allure-results --clean-alluredir`
> so raw Allure data is always written on every test run.

---

## Allure Report

After each run the Allure HTML report is generated at `allure-report/index.html`.

The report includes:
- ✅ Test results (pass / fail / broken)
- 📸 Full-page screenshot on test completion
- 📄 Text attachments (error messages, product names, price breakdowns)
- 🎬 Video recording of each test (saved under `allure-results/videos/`)
- 🪜 Step-by-step execution log for every test

---

## Test Scenarios

### Q1 — Locked Out User (20 Marks)
**File:** `tests/test_q1_locked_out_user.py`

1. Navigate to https://www.saucedemo.com
2. Enter username `locked_out_user` / password `secret_sauce`
3. Click Login
4. Assert error banner is visible
5. Assert error text equals:
   > `Epic sadface: Sorry, this user has been locked out.`
6. Assert user remains on the login page

---

### Q2 — Standard User Full Journey (50 Marks)
**File:** `tests/test_q2_standard_user.py`

1. Login as `standard_user`
2. **Reset App State** via hamburger menu → verify cart is empty
3. Add **3 specific items** to cart:
   - Sauce Labs Backpack
   - Sauce Labs Bike Light
   - Sauce Labs Bolt T-Shirt
4. Verify cart badge shows **3**
5. Navigate → Cart → Checkout
6. Fill customer info (John Doe, 12345)
7. On **Overview page** verify:
   - All 3 product names match
   - Subtotal = sum of item prices
   - Grand total = subtotal + tax
8. Click **Finish** → verify success header:
   > `Thank you for your order!`
9. Navigate back → **Reset App State** (second time)
10. **Logout** → verify login page

---

### Q3 — Performance Glitch User (30 Marks)
**File:** `tests/test_q3_performance_glitch_user.py`

1. Login as `performance_glitch_user` (extended timeout for glitch delay)
2. **Reset App State** → verify cart empty
3. Sort products **Name (Z to A)**
4. Add the **first product** from the sorted list to cart
5. Navigate → Cart → Checkout
6. Fill customer info (Jane Smith, 67890)
7. On **Overview page** verify:
   - Product name matches the selected item
   - Subtotal = item price
   - Grand total = subtotal + tax
8. Click **Finish** → verify success header:
   > `Thank you for your order!`
9. Navigate back → **Reset App State** (second time)
10. **Logout** → verify login page

---

## Credentials Reference

| Username | Password | Status |
|---|---|---|
| `standard_user` | `secret_sauce` | ✅ Normal user |
| `locked_out_user` | `secret_sauce` | 🔒 Blocked |
| `performance_glitch_user` | `secret_sauce` | 🐢 Slow responses |

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `playwright install` fails | Run `playwright install-deps` first (Linux) |
| `allure: command not found` | Install Allure CLI (see Prerequisites) |
| Tests timeout on Q3 | `performance_glitch_user` is slow by design — timeouts are extended to 20 s |
| `ModuleNotFoundError: pages` | Ensure you run pytest from the project root, not from inside `tests/` |
| Port conflict on `allure open` | Use `allure open allure-report -p 9999` to pick a custom port |
