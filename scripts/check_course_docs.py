#!/usr/bin/env python3
"""Check course links and runnable references without pretending to run ROS."""

import ast
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit


def heading_anchors(text):
    """Return GitHub-style anchors for the headings used in these notes."""
    anchors = set()
    counts = {}
    for heading in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', text, re.MULTILINE):
        slug = re.sub(r'[^\w\- ]', '', heading.lower()).replace(' ', '-')
        count = counts.get(slug, 0)
        anchors.add(f'{slug}-{count}' if count else slug)
        counts[slug] = count + 1
    return anchors


def check_links(path, text):
    """Check relative link targets and local Markdown heading fragments."""
    errors = []
    for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^\s)]+)\)', text):
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc:
            continue
        destination = path.parent / unquote(parsed.path) if parsed.path else path
        if not destination.exists():
            errors.append(f'{path}: missing link target {target}')
        elif parsed.fragment and destination.suffix == '.md':
            if unquote(parsed.fragment) not in heading_anchors(destination.read_text()):
                errors.append(f'{path}: missing heading {target}')
    return errors


def package_executables(root):
    """Read literal console-script declarations without executing setup.py."""
    packages = {}
    for package in (root / 'src').iterdir():
        if not package.is_dir():
            continue
        names = set()
        setup = package / 'setup.py'
        if setup.exists():
            for node in ast.walk(ast.parse(setup.read_text())):
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    match = re.fullmatch(r'([\w-]+)\s*=\s*[\w.]+:main', node.value)
                    if match:
                        names.add(match[1])
        packages[package.name] = names
    return packages


def check_commands(root, path, text, packages):
    """Validate shell syntax and repository-owned executable/file references."""
    errors = []
    for block in re.findall(r'```bash\n(.*?)```', text, re.DOTALL):
        result = subprocess.run(['bash', '-n'], input=block, text=True,
                                capture_output=True, check=False)
        if result.returncode:
            errors.append(f'{path}: shell syntax: {result.stderr.strip()}')
    # Also inspect inline commands. External ROS tools need runtime validation.
    for action, package, name in re.findall(
            r'ros2\s+(run|launch)\s+([\w-]+)\s+([\w.\-]+)', text):
        if package not in packages:
            continue
        if action == 'run' and name not in packages[package]:
            errors.append(f'{path}: unknown executable {package} {name}')
        if action == 'launch' and not (root / 'src' / package / 'launch' / name).is_file():
            errors.append(f'{path}: missing launch file {package} {name}')
    for source in re.findall(r'python3\s+(src/[\w./-]+)', text):
        if not (root / source).is_file():
            errors.append(f'{path}: missing Python source {source}')
    return errors


def validate(root):
    """Return diagnostics and counts for this repository's written companion."""
    errors = []
    documents = [root / 'README.md', *sorted((root / 'course_lectures').rglob('*.md'))]
    packages = package_executables(root)
    blocks = 0
    for path in documents:
        text = path.read_text()
        if len(re.findall(r'^```', text, re.MULTILINE)) % 2:
            errors.append(f'{path}: unbalanced code fences')
        blocks += len(re.findall(r'^```bash$', text, re.MULTILINE))
        errors.extend(check_links(path, text))
        errors.extend(check_commands(root, path, text, packages))
    sections = '\n'.join(p.read_text() for p in (root / 'course_lectures/sections').glob('*.md'))
    lectures = [int(n) for n in re.findall(r'^## Lecture (\d+):', sections, re.MULTILINE)]
    if sorted(lectures) != list(range(1, 84)):
        errors.append('Section descriptions must preserve exactly Lectures 1–83.')
    core = (root / 'course_lectures/core-practical-checkpoints.md').read_text()
    if {int(n) for n in re.findall(r'^### Lecture (\d+)', core, re.MULTILINE)} != set(range(3, 40)):
        errors.append('Core checkpoints must cover every Lecture 3–39.')
    applied = (root / 'course_lectures/applied-practical-checkpoints.md').read_text()
    applied_numbers = {int(n) for n in re.findall(r'^\| (\d+) \|', applied, re.MULTILINE)}
    if applied_numbers != set(range(40, 83)) or '## Lecture 83:' not in applied:
        errors.append('Applied checkpoints must cover every Lecture 40–83.')
    return errors, len(documents), blocks


def main():
    """Exit nonzero for broken references; report the limits of the check."""
    root = Path(__file__).resolve().parents[1]
    errors, documents, blocks = validate(root)
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        print(f'FAILED: {len(errors)} documentation errors.', file=sys.stderr)
        return 1
    print(f'PASS: {documents} Markdown files, {blocks} Bash blocks, local links, '
          'lecture coverage and repository command targets.')
    print('Not tested: external URLs, installed ROS commands, DDS, simulation, '
          'navigation, perception or other runtime behavior.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
