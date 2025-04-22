#!/usr/bin/env python3
import os
import getpass
import socket
import subprocess
from datetime import datetime
from colorama import init, Fore, Style
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit import ANSI
from prompt_toolkit.completion import PathCompleter
os.environ["SHELL"] = "/usr/bin/psh"


path_completer = PathCompleter()
session = PromptSession(completer=path_completer)


# Initialize Colorama (automatically resets colors after each print)
init(autoreset=True)

# Sample commands for autocompletion
commands = ["ls", "cd", "echo", "cat", "mkdir", "exit"]
completer = WordCompleter(commands, ignore_case=True)

# History file
history_file = os.path.expanduser("~/.pyfish_history")

# PromptSession
session = PromptSession(
    completer=completer,
    history=FileHistory(history_file),
    auto_suggest=AutoSuggestFromHistory(),
)

def get_git_branch():
    try:
        subprocess.check_output(['git', 'rev-parse', '--is-inside-work-tree'],
                                stderr=subprocess.PIPE)
        branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']) \
                         .strip().decode('utf-8')
        return branch
    except subprocess.CalledProcessError:
        return None

def get_time():
    return datetime.now().strftime("%I:%M:%p")

def get_prompt():
    user     = getpass.getuser()
    hostname = socket.gethostname()
    cwd      = os.getcwd()
    parts    = cwd.split(os.sep)[1:]
    path     = ">".join(parts) if parts else "~"

    branch = get_git_branch()
    branch_str = f" {Fore.MAGENTA}({branch})" if branch else ""

    time_str = get_time()

    # Color assignments
    u_col = Fore.CYAN
    h_col = Fore.GREEN
    p_col = Fore.YELLOW
    t_col = Fore.RED
    sym   = Fore.BLUE + "$>"

    # Build the prompt
    prompt = (
        f"{u_col}{user}"
        f"{Style.RESET_ALL}{h_col}@{hostname}"
        f"{Style.RESET_ALL}{p_col}>{path}"
        f"{Style.RESET_ALL}{branch_str}"
        f"{Style.RESET_ALL} {t_col}{time_str}"
        f"{Style.RESET_ALL}{sym} "
    )
    return ANSI(f"{prompt}")  # Wrap the string in ANSI for proper handling

def run_command(cmd):
    if not cmd.strip():
        return
    parts = cmd.split()
    if parts[0] == "cd":
        try:
            os.chdir(parts[1] if len(parts) > 1 else os.path.expanduser("~"))
        except Exception as e:
            print(f"{Fore.RED}cd: {e}{Style.RESET_ALL}")
    else:
        os.system(cmd)

pshrc_path = os.path.expanduser("~/.pshrc")
if os.path.exists(pshrc_path):
    with open(pshrc_path) as f:
        for line in f:
            os.system(line.strip())


def main():
   # print(f"{Fore.GREEN}Welcome to P-Shell{Style.RESET_ALL} - type 'exit' to quit.")
    while True:
        try:
            prompt = get_prompt()
            cmd = session.prompt(prompt)
            if cmd.strip() == "exit":
              #  print(f"{Fore.GREEN}Deactivated. Good Bye!{Style.RESET_ALL}")
                break
            run_command(cmd)
        except (KeyboardInterrupt, EOFError):
            break

if __name__ == "__main__":
    main()
