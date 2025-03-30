import argparse
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

from bs4 import BeautifulSoup, Tag
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


def find_issues() -> list[Issue]:
    result = []
    count = 0
    try:
        gh = Github(auth=auth)
        issues = gh.search_issues(query=f'label:"{args.label}" language:{args.language} is:open')

        while True:
            for issue in issues:
                count += 1
                if issue.repository.stargazers_count >= args.stars:
                    result.append(issue)

                if count == args.limit:
                    return result
    except Exception as e:
        print('Error occurred', e)
    return result


def create_row(issue: Issue) -> Tag|None:
    soup = BeautifulSoup('', features='html.parser')
    try:
        row = soup.new_tag('tr')

        # Create repository link
        repo_cell = soup.new_tag('td')
        repo_link = soup.new_tag('a', href=issue.repository.html_url, target="_blank")
        repo_link.string = issue.repository.full_name
        repo_cell.append(repo_link)

        # Create issue link
        issue_cell = soup.new_tag('td')
        issue_link = soup.new_tag('a', href=issue.html_url, target="_blank")
        issue_link.string = f'Issues#{issue.number}'
        issue_cell.append(issue_link)

        # Create stars count
        stars_cell = soup.new_tag('td')
        stars_cell.string = str(issue.repository.stargazers_count)

        # Append the cells to the row
        row.append(repo_cell)
        row.append(issue_cell)
        row.append(stars_cell)
    except Exception as e:
        print('Error occurred', e)


def create_table_rows(soup: BeautifulSoup, issues: list[Issue]):
    table_body = soup.find(id='issues-table').find('tbody')
    table_body.clear()

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(create_row, issue) for issue in issues]

        for future in as_completed(futures):
            if row := future.result():
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
