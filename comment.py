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


def get_latest_pull_request(data: dict) -> int:
    """Gets the latest pull request given `data.
    
    Args:
        data: The JSON dictionary of pull requests data.
        
    Returns:
        The ID of the latest pull request.
    """
    return max([pr['id'] for pr in data['values']])


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


def main(argv: sys.argv[1:] = List[str]) -> int:
    """Adds a PR comment to a specified PR.
    
    Returns:
        Status code of comment attempt.
    """
    if len(argv) != 1:
        print('Must specify comment to post', file=sys.stderr)
        return 500
    comment = argv[1]
    status_code, pr_data = get_pull_requests()
    if status_code >= 400:
        return status_code
    latest_pr = get_latest_pull_request(pr_data)
    status_code = add_pull_request_comment(latest_pr, comment)
    return status_code


if __name__ == '__main__':
    sys.exit(main())
