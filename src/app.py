import argparse
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import groupby

from bs4 import BeautifulSoup
from github import Github
from github.Auth import Token
from github.Issue import Issue

auth = Token(os.getenv('GITHUB_TOKEN'))

parser = argparse.ArgumentParser(prog='gh-issue-finder', description='helps in finding github issues')
parser.add_argument('--label', help='label to find')
parser.add_argument('--language', help='language to find')
parser.add_argument('--limit', default=500, type=int, required=False, help='Minimum number of issues to search')
parser.add_argument('-s', '--stars', default=10, type=int, required=False, help='minimum number of stars')
args = parser.parse_args(sys.argv[1:])


def filter_issue(issue: Issue) -> Issue | None:
    try:
        if issue.repository.stargazers_count >= args.stars:
            return issue
    except Exception as e:
        print('Error occurred:', e)


def find_issues() -> list[Issue]:
    result = []
    try:
        gh = Github(auth=auth)
        issues = gh.search_issues(query=f'label:"{args.label}" language:{args.language} is:open')

        futures = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            for issue in issues:
                futures.append(executor.submit(filter_issue, issue))
                if len(futures) == args.limit:
                    break

        for future in as_completed(futures):
            if issue := future.result():
                result.append(issue)
    except Exception as e:
        print('Error occurred', e)
    return result


def create_table_rows(soup: BeautifulSoup, issues: list[Issue]):
    table_body = soup.find(id='issues-table').find('tbody')
    table_body.clear()
    key = lambda x: x.repository.full_name

    for _, issue_group in groupby(sorted(issues, key=key), key=key):
        row = soup.new_tag('tr')
        repo = None

        # Create issue links
        issue_cell = soup.new_tag('td')
        issue_list = soup.new_tag('ul')
        for issue in issue_group:
            issue_list_element = soup.new_tag('li')
            issue_link = soup.new_tag('a', href=issue.html_url, target="_blank")
            issue_link.string = f'Issues#{issue.number}'
            issue_list_element.append(issue_link)
            issue_list.append(issue_list_element)
            repo = issue.repository
        issue_cell.append(issue_list)

        if not repo:
            continue

        # Create repository link
        repo_cell = soup.new_tag('td')
        repo_link = soup.new_tag('a', href=repo.html_url, target="_blank")
        repo_link.string = repo.full_name
        repo_cell.append(repo_link)



        # Create stars count
        stars_cell = soup.new_tag('td')
        stars_cell.string = str(repo.stargazers_count)

        # Append the cells to the row
        row.append(repo_cell)
        row.append(issue_cell)
        row.append(stars_cell)

        table_body.append(row)


def find_issues_and_populate_html() -> None:
    issues = find_issues()
    with open('src/template.html') as fp, open('index.html', 'w') as fw:
        soup = BeautifulSoup(fp, features='html.parser')
        create_table_rows(soup, issues)
        fw.write(soup.prettify())


def main():
    find_issues_and_populate_html()


if __name__ == '__main__':
    main()
