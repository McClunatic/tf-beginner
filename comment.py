import argparse
import os
import subprocess as sp
import sys
from typing import List, Tuple

import requests

BITBUCKET = 'https://bitbucket.nnlscience.onmicrosoft.com:8443'
PROJECT = 'DAT'
REPO = 'tf-beginner'


def get_pull_requests(session: requests.Session) -> Tuple[int, dict]:
    """Gets pull requests data.

    Args:
        session: The session object with auth set up.

    Returns:
        JSON response from Bitbucket containing pull requests data.
    """
    url = (
        f'{BITBUCKET}/rest/api/latest/projects/{PROJECT}/repos/{REPO}/'
        'pull-requests')
    r = session.get(url=url, verify=False)
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
        pr for pr in data['values'] if pr['fromRef']['displayId'] == branch]
    try:
        return max([pr['id'] for pr in branch_data])
    except ValueError:
        # TODO: find out branch info
        return max([pr['id'] for pr in data['values']])

def add_pull_request_comment(
    session: requests.Session,
    pr: int,
    comment: str,
) -> int:
    """Adds `comment` to pull request with ID `pr`.

    Args:
        session: The requests Session object with auth set up.
        pr: The ID of the PR to comment on.
        comment: The comment to add.

    Returns:
        The status code for the POST request.
    """
    url = (
        f'{BITBUCKET}/rest/api/latest/projects/{PROJECT}/repos/{REPO}/'
        f'pull-requests/{pr}/comments')
    r = session.post(url=url, json={'text': comment}, verify=False)
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


def main(argv: List[str] = sys.argv[1:]) -> int:
    """Adds a PR comment to a specified PR.

    Returns:
        Status code of comment attempt.
    """
    args = get_parser().parse_args(argv)
    comment = open(args.file).read() if args.file else args.comment
    with requests.Session() as session:
        if 'USERNAME' not in os.environ or 'PASSWORD' not in os.environ:
            print('Failed to get credentials')
            return 500
        session.auth = (os.environ['USERNAME'], os.environ['PASSWORD'])
        status_code, pr_data = get_pull_requests(session)
        if status_code >= 400:
            print('Failed to get PR data')
            return status_code
        branch_pr = get_branch_pull_request(pr_data)
        status_code = add_pull_request_comment(session, branch_pr, comment)
        if status_code >= 400:
            print('Failed to add PR comment')
        return 0 if status_code == 201 else status_code


if __name__ == '__main__':
    sys.exit(main())
