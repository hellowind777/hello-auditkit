#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audit Report Save Script
Saves audit report to file with standardized naming convention.

Cross-platform compatible: Windows, macOS, Linux

Usage:
    # Windows (use -X utf8 for Chinese support):
    python -X utf8 save_report.py --project "<name>" --output-dir "<path>" --content "<text>"

    # macOS/Linux:
    python3 save_report.py --project "<name>" --output-dir "<path>" --content "<text>"

    # Via stdin (all platforms):
    echo "<report>" | python3 save_report.py --project "<name>" --output-dir "<path>"

Arguments:
    --project, -p      Project name (used in filename)
    --output-dir, -o   Directory to save the report
    --content, -c      Report content (optional, reads from stdin if not provided)

Output filename format: 审计报告_{project}_{YYYYMMDD_HHmmss}.md

Note:
    - Windows: Use -X utf8 flag for proper Chinese character handling
    - All platforms: Quote paths with double quotes for spaces/Chinese characters
    - macOS/Linux: May need to run `chmod +x save_report.py` for direct execution
"""

import argparse
import sys
import os
import io
import platform
from datetime import datetime

# Ensure UTF-8 encoding for stdout/stderr (primarily for Windows)
def setup_utf8_encoding():
    """Configure UTF-8 encoding for console output."""
    if platform.system() == 'Windows':
        # Windows needs explicit UTF-8 configuration
        if sys.stdout.encoding != 'utf-8':
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        if sys.stderr.encoding != 'utf-8':
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
        if sys.stdin.encoding != 'utf-8':
            sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')

setup_utf8_encoding()


def save_report(project_name: str, output_dir: str, content: str) -> str:
    """
    Save audit report to file.

    Args:
        project_name: Name of the audited project
        output_dir: Directory to save the report
        content: Report content

    Returns:
        Full path of the saved report file
    """
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create filename
    filename = f"审计报告_{project_name}_{timestamp}.md"

    # Full path
    filepath = os.path.join(output_dir, filename)

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Write report
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return filepath


def main():
    parser = argparse.ArgumentParser(
        description='Save audit report to file with standardized naming.'
    )
    parser.add_argument(
        '--project', '-p',
        required=True,
        help='Project name (used in filename)'
    )
    parser.add_argument(
        '--output-dir', '-o',
        required=True,
        help='Directory to save the report'
    )
    parser.add_argument(
        '--content', '-c',
        help='Report content (reads from stdin if not provided)'
    )

    args = parser.parse_args()

    # Get content from argument or stdin
    if args.content:
        content = args.content
    else:
        # Read from stdin
        if sys.stdin.isatty():
            print("Error: No content provided. Use --content or pipe content via stdin.", file=sys.stderr)
            sys.exit(1)
        content = sys.stdin.read()

    if not content.strip():
        print("Error: Report content is empty.", file=sys.stderr)
        sys.exit(1)

    try:
        filepath = save_report(args.project, args.output_dir, content)
        # Output the saved path (this is the main output for the caller to capture)
        print(filepath)
    except Exception as e:
        print(f"Error: Failed to save report: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
