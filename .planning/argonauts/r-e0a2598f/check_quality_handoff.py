"""Fail-closed handoff process check; never an independent product verdict."""
import argparse
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--handoff", required=True)
    parser.parse_args()
    print("implementation_pending: handoff validation not implemented", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
