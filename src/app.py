import argparse
import os
import sys
from argparse import Namespace

from github import Github
from github.Auth import Token

auth = Token(os.getenv('GITHUB_TOKEN'))

parser = argparse.ArgumentParser(prog='gh-issue-finder', description='helps in finding github issues')
parser.add_argument('--label', help='label to find')
parser.add_argument('--language', help='language to find')
parser.add_argument('--limit', default=500, type=int, required=False, help='Minimum number of issues to search')
parser.add_argument('-s', '--stars', default=10, type=int, required=False, help='minimum number of stars')


def find_issues(args: Namespace) -> list:
    result = []
    count = 0
    try:
        gh = Github(auth=auth)
        issues = gh.search_issues(query=f'label:"{args.label}" language:{args.language} is:open')

        while True:
            for issue in issues:
                count += 1
                if issue.repository.stargazers_count < args.stars:
                    result.append(issue)

                if count == args.limit:
                    return result
    except Exception as e:
        print('Error occurred', e)
    return result


def main():
    iss = find_issues(parser.parse_args(sys.argv[1:]))
    print(iss)


if __name__ == '__main__':
    main()
