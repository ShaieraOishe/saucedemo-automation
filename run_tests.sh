#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# run_tests.sh
# Convenience script to run Q1, Q2, Q3 tests individually or all together.
#
# Usage:
#   ./run_tests.sh          → runs ALL tests sequentially
#   ./run_tests.sh q1       → runs Q1 only
#   ./run_tests.sh q2       → runs Q2 only
#   ./run_tests.sh q3       → runs Q3 only
#   ./run_tests.sh report   → generates & opens Allure report (no test run)
# ─────────────────────────────────────────────────────────────────────────────

set -e

RESULTS_DIR="allure-results"
REPORT_DIR="allure-report"

run_allure_report() {
  echo ""
  echo "══════════════════════════════════════════"
  echo " Generating Allure Report..."
  echo "══════════════════════════════════════════"
  allure generate "$RESULTS_DIR" --clean -o "$REPORT_DIR"
  echo " Report saved to: $REPORT_DIR/index.html"
  echo " Opening report in browser..."
  allure open "$REPORT_DIR"
}

case "${1:-all}" in
  q1)
    echo "▶ Running Q1 — Locked Out User..."
    pytest tests/test_q1_locked_out_user.py -v
    ;;
  q2)
    echo "▶ Running Q2 — Standard User Purchase Journey..."
    pytest tests/test_q2_standard_user.py -v
    ;;
  q3)
    echo "▶ Running Q3 — Performance Glitch User Journey..."
    pytest tests/test_q3_performance_glitch_user.py -v
    ;;
  all)
    echo "▶ Running ALL tests sequentially (Q1 → Q2 → Q3)..."
    pytest tests/test_q1_locked_out_user.py \
           tests/test_q2_standard_user.py \
           tests/test_q3_performance_glitch_user.py -v
    ;;
  report)
    run_allure_report
    exit 0
    ;;
  *)
    echo "Unknown option: $1"
    echo "Usage: ./run_tests.sh [q1|q2|q3|all|report]"
    exit 1
    ;;
esac

run_allure_report
