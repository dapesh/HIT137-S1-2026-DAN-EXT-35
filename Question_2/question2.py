"""Question 2 wrapper.

Use evaluator.py for the required assignment interface.
This file is kept as a convenience CLI entry point.
"""

from evaluator import evaluate_file, main

__all__ = ["evaluate_file", "main"]


if __name__ == "__main__":
    main()