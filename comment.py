import argparse
import subprocess as sp
import sys
from typing import List, Tuple

import requests

BITBUCKET = 'https://bitbucket.nnlscience.onmicrosoft.com:8443/'
PROJECT = 'DAT'
REPO = 'tf-beginner'


def get_pull_requests() -> Tuple[int, dict]:
    """Gets pull requests data.
    
    Returns:
        JSON response from Bitbucket containing pull requests data.
    """
    url = (
        f'{BITBUCKET}/rest/api/latest/projects/{PROJECT}/repos/{REPO}/'
        'pull-requests')
    r = requests.get(url=url)
    return r.status_code, r.json() if r.status_code < 400 else {}


def get_branch_pull_request(data: dict) -> int:
    """Gets the branch pull request given `data`.
    
    Args:
        data: The JSON dictionary of pull requests data.
        
    Returns:
        The ID of the branch's pull request.
    """
    cproc = sp.run('git rev-parse --abbrev-ref HEAD'.split(), stdout=sp.PIPE)
    branch = cproc.stdout.decode().strip()
    branch_data = [
        pr for pr in data['values'] if pr['fromRef']['displayID'] == branch]
    return max([pr['id'] for pr in branch_data['values']])

def add_pull_request_comment(pr: int, comment: str) -> int:
    """Adds `comment` to pull request with ID `pr`.

    Args:
        pr: The ID of the PR to comment on.
        comment: The comment to add. 

    Returns:
        The status code for the POST request.
    """
    url = (
        f'{BITBUCKET}/rest/api/latest/projects/{PROJECT}/repos/{REPO}/'
        f'pull-requests/{pr}/comments')
    r = requests.post(url=url, data={'text': comment})
    return r.status_code


def get_parser() -> argparse.ArgumentParser:
    """Gets the comment script argument parser.
    
    Returns:
        The parser.
    """
    parser = argparse.ArgumentParser(description='Add a comment to the PR.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--comment', help='Comment string to add')
    group.add_argument('--file', help='File name to read comment from')
    return parser


def main(argv: sys.argv[1:] = List[str]) -> int:
    """Adds a PR comment to a specified PR.
    
    Returns:
        Status code of comment attempt.
    """
    args = get_parser().parse_args(argv)
    comment = open(args.file).read() if args.file else args.comment
    status_code, pr_data = get_pull_requests()
    if status_code >= 400:
        return status_code
    branch_pr = get_branch_pull_request(pr_data)
    status_code = add_pull_request_comment(branch_pr, comment)
    return status_code


if __name__ == '__main__':
    sys.exit(main())
