# Test Action

1. Read current-feature.md to understand what was implemented
2. Identify pure functions (non-interactive logic) added/modified for this feature
3. Check if tests already exist for these functions
4. For functions without tests that have testable logic, write unit tests:
   - Use plain `assert` statements or `unittest` from the Python standard library
   - Focus on the core algorithmic functions (not the interactive input()/print() CLI)
   - Test happy path and edge/error cases (e.g. unique solution, infinite solutions, no solution, need for pivoting)
   - Do not write tests just to write them. Use your best judgement
5. Run the tests (e.g. `python3 path/to/test_file.py`) to verify all tests pass
6. Report test coverage for the new feature code
