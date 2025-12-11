#!/usr/bin/env python3
"""Wi-Tri Lab — interactive terminal teacher
Run: python3 start.py
Options:
  --lesson N    # open lesson N starter in editor
  --check N     # run automated checker for lesson N
  --resources N # show resources for lesson N
"""
import os, sys, argparse, subprocess
from pathlib import Path

ROOT = Path(__file__).parent
LESSONS_DIR = ROOT / 'lessons'
LESSONS = sorted([p for p in LESSONS_DIR.iterdir() if p.is_dir()])
WIWI = r"""

 .--.
|o_o |
|:_/ |
 //   \\ \\
(|  ^  | )  wiwi
/'\_   _/`\\
\\___)=(___/

"""

def list_lessons():
    for i,p in enumerate(LESSONS, start=1):
        print(f"{i:02d}. {p.name.replace('_',' ')}")

def show_file(path):
    print('---')
    with open(path,'r', encoding='utf-8') as f:
        print(f.read())
    print('---')

def open_editor(path):
    editor = os.environ.get('EDITOR','nano')
    subprocess.call([editor, str(path)])

def check_lesson(num):
    p = LESSONS[num-1]
    checker = p / 'checker.py'
    if checker.exists():
        print("Running checker (may need sudo for network related tests)...")
        subprocess.call([sys.executable, str(checker)])
    else:
        print("No automated checker for this lesson. Manual review.")

def show_resources(num):
    p = LESSONS[num-1]
    res = p / 'resources.txt'
    if res.exists():
        show_file(res)
    else:
        rglob = ROOT / 'resources'
        for f in sorted(rglob.iterdir()):
            print(f.name)
        print("Use --resources N to view lesson specific resources.")

def main():
    print(WIWI)
    print("Welcome to Wi-Tri Lab — built by 0xDiddy\n")
    ap = argparse.ArgumentParser()
    ap.add_argument('--lesson', type=int)
    ap.add_argument('--check', type=int)
    ap.add_argument('--resources', type=int)
    args = ap.parse_args()

    if args.resources:
        if 1 <= args.resources <= len(LESSONS):
            show_resources(args.resources)
        else:
            print("Invalid lesson number for resources.")
        return

    if args.check:
        if 1 <= args.check <= len(LESSONS):
            check_lesson(args.check)
        else:
            print("Invalid lesson number for check.")
        return

    while True:
        print('\nLessons:')
        list_lessons()
        choice = input('\nEnter lesson number (q to quit): ').strip()
        if choice.lower() in ('q','quit'):
            print('Later hacker. Ship something.')
            break
        try:
            n = int(choice)
            lesson = LESSONS[n-1]
        except Exception:
            print('Invalid choice')
            continue

        print(f"\n--- {lesson.name} ---")
        intro = lesson / 'intro.txt'
        if intro.exists():
            show_file(intro)
        starter = lesson / 'starter.py'
        if starter.exists():
            print('\nOpening starter.py in your editor. Save and exit when done.')
            open_editor(starter)
            print(f'\nRun/Check your work: python3 start.py --check {n}')
        else:
            print('Starter not found for this lesson.')

if __name__=='__main__':
    main()
