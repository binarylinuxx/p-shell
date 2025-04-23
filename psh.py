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

# Set environment variable for shell
os.environ["SHELL"] = "/usr/bin/psh"

# Initialize Colorama (automatically resets colors after each print)
init(autoreset=True)

# --- Configuration ---
history_file = os.path.expanduser("~/.psh_history")
pshrc_path = os.path.expanduser("~/.pshrc")

# Command autocompletion list
commands = [
    # Basic commands
    'ls', 'cd', 'pwd', 'cat', 'echo', 'exit', 'clear', 'history', 'man',
    # File management
    'cp', 'mv', 'rm', 'mkdir', 'rmdir', 'touch', 'chmod', 'chown', 'ln', 'find', 'grep',
    # System commands
    'ps', 'top', 'htop', 'kill', 'pkill', 'df', 'du', 'free', 'uname', 'whoami',
    # Network
    'ping', 'ifconfig', 'ip', 'netstat', 'ssh', 'scp', 'wget', 'curl', 'nc', 'dig',
    # Package managers
    'apt', 'yum', 'dnf', 'pacman', 'pip', 'npm',
    # Development
    'git', 'python', 'python3', 'gcc', 'g++', 'make', 'cmake', 'docker', 'kubectl',
    # Text editors
    'nano', 'vim', 'vi', 'emacs', 'sed', 'awk',
    # Archives
    'tar', 'gzip', 'gunzip', 'zip', 'unzip',
    # Miscellaneous
    'date', 'cal', 'bc', 'shutdown', 'reboot', 'alias', 'export', 'source', 'sudo', 'su'
]

# --- Setup Completers and Session ---
completer = WordCompleter(commands, ignore_case=True)
path_completer = PathCompleter()

session = PromptSession(
    completer=completer,
    history=FileHistory(history_file),
    auto_suggest=AutoSuggestFromHistory(),
)

# --- Helper Functions ---
def get_git_branch():
    """Returns current Git branch or None if not in a repo."""
    try:
        subprocess.check_output(['git', 'rev-parse', '--is-inside-work-tree'],
                              stderr=subprocess.PIPE)
        branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
        return branch.strip().decode('utf-8')
    except (subprocess.CalledProcessError, Exception):
        return None

def get_time():
    """Returns formatted time (e.g., '07:55PM')."""
    return datetime.now().strftime("%I:%M%p")

def get_prompt():
    """Generates the colored shell prompt."""
    user = getpass.getuser()
    hostname = socket.gethostname()
    cwd = os.getcwd()
    
    # Shorten path (e.g., /home/user -> ~, /home/user/projects -> ~>projects)
    parts = cwd.split(os.sep)[1:]
    path = ">".join(parts) if parts else "~"

    # Git branch (only show if in a repo)
    branch = get_git_branch()
    branch_str = f" {Fore.MAGENTA}({branch})" if branch else ""

    # Build prompt components
    prompt = (
        f"{Fore.CYAN}{user}"
        f"{Style.RESET_ALL}{Fore.GREEN}@{hostname}"
        f"{Style.RESET_ALL}{Fore.YELLOW}>{path}"
        f"{Style.RESET_ALL}{branch_str}"
        f"{Style.RESET_ALL} {Fore.RED}{get_time()}"
        f"{Style.RESET_ALL}{Fore.BLUE}$> "
    )
    return ANSI(prompt)

def run_command(cmd):
    """Executes shell commands or built-ins like 'cd'."""
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

# --- Main Shell Loop ---
def main():
    # Load .pshrc if it exists
    if os.path.exists(pshrc_path):
        with open(pshrc_path) as f:
            for line in f:
                os.system(line.strip())

    while True:
        try:
            cmd = session.prompt(get_prompt())
            if cmd.strip() == "exit":
                print("good bye!") 
                break
            run_command(cmd)
        except (KeyboardInterrupt, EOFError):
            print()  # Newline on Ctrl+C
            break

if __name__ == "__main__":
    main()
