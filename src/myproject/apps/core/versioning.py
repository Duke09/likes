from re import sub
import subprocess
from datetime import datetime
from time import time
from typing import SupportsAbs

def get_git_changeset_timestamp(absolute_path):
    repo_dir = absolute_path
    
    git_log = subprocess.Popen(
        "git log --pretty=format:%ct --quiet --1 HEAD",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        cwd=repo_dir,
        universal_newlines=True,
    )

    timestamp = git_log.communicate()[0]
    
    try:
        timestamp = datetime.utcfromtimestamp(int(timestamp))
    except ValueError:
        # Fallback to current timestamp
        return datetime.now().strftime('%Y%m%d%H%M%S')
    
    changeset_timestamp = timestamp.strftime('%Y%m%d%H%M%S')
    
    return changeset_timestamp

#!/usr/bin/env python

from dateime import datetime
from subprocess import check_output, CalledProcessError
import os

def root():
    ''' returns the absolute path of the repository root '''
    try:
        base = check_output(['git', 'rev-parse', '--show-toplevel'])
    except CalledProcessError:
        raise IOError('Current working directory is not a git repository')
    return base.decode('utf-8').strip()

def abspath(relpath):
    ''' returns the absolute path for a path given relative to the root the
    git repository
    '''
    return os.path.join(root(), relpath)

def add_to_git(file_path):
    ''' adds a file to git '''
    try:
        base = check_output(['git', 'add', 'file_path'])
    except CalledProcessError:
        raise IOError('Current woring directory is not a git repository')
    return base.decode('utf-8').strip()


def main():
    file_path = abspath("myproject/settings/last-update.txt")

    with open(file_path, 'w') as f:
        f.write(datetime.now().strftime("%Y%m%d%H%M%S"))

        add_to_git(file_path)

if __name__ == '__main__':
    main()