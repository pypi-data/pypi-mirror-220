"""
Module to get a random LeetCode question according to certain
parameters and then output a local Python file to work on
said question.
"""


import random
from pathlib import Path
from typing import Literal

import requests
from bs4 import BeautifulSoup

ROOT = 'https://leetcode.com'
API_URL = f'{ROOT}/api/problems/all/'
GQL_URL = f'{ROOT}/graphql'

SLUG_KEY = 'question__title_slug'


def query_all_questions() -> dict:
    """Query LeetCode API for index of all questions"""
    return requests.get(API_URL, timeout=5).json()['stat_status_pairs']


def choose_a_valid_question(
        questions: list[dict],
        max_difficulty: Literal[1, 2, 3],
        min_difficulty: Literal[1, 2, 3],
    ) -> dict:
    """Recurse until a valid question is found, return its slug"""
    choice = random.choice(questions)
    if any((
        choice['paid_only'],
        choice['difficulty']['level'] < min_difficulty,
        choice['difficulty']['level'] > max_difficulty,
        choice['stat'].get(SLUG_KEY) is None,
    )):
        return choose_a_valid_question(
            questions,
            max_difficulty,
            min_difficulty,
        )
    return choice['stat'][SLUG_KEY]


def get_question_data(question_slug: dict) -> dict:
    """Get all metadata available for question via GraphQL query"""
    return requests.post(GQL_URL, timeout=10, json={
        'operationName': 'questionData',
        'variables': {
            'titleSlug': question_slug,
        },
        'query': """query questionData($titleSlug: String!) {
                        question(titleSlug: $titleSlug) {
                            questionId
                            questionFrontendId
                            boundTopicId
                            title
                            titleSlug
                            content
                            translatedTitle
                            translatedContent
                            isPaidOnly
                            difficulty
                            likes
                            dislikes
                            isLiked
                            similarQuestions
                            contributors {
                                username
                                profileUrl
                                avatarUrl
                                __typename
                            }
                            langToValidPlayground
                            topicTags {
                                name
                                slug
                                translatedName
                                __typename
                            }
                            companyTagStats
                            codeSnippets {
                                lang
                                langSlug
                                code
                                __typename
                            }
                            stats
                            hints
                            solution {
                                id
                                canSeeDetail
                                __typename
                            }
                            status
                            sampleTestCase
                            metaData
                            judgerAvailable
                            judgeType
                            mysqlSchemas
                            enableRunCode
                            enableTestMode
                            envInfo
                            libraryUrl
                            __typename
                        }
                    }
                """,
    }).json()


def parse_question_details(question_data: dict) -> dict[str, str]:
    """Parse response from GraphQL down into data needed for output"""
    soup = BeautifulSoup(question_data['data']['question']['content'], 'lxml')
    return {
        'difficulty': question_data['data']['question']['difficulty'],
        'question_id': question_data['data']['question']['questionId'],
        'question': soup.get_text(),
        'test_case': question_data['data']['question']['sampleTestCase'],
        'title': question_data['data']['question']['title'],
    }


def output_python_file(
        output_path: Path,
        question_details: dict[str, str],
    ) -> None:
    """Take question details and output a python file shell"""
    difficulty, qid, question, test_case, title = (
        question_details['difficulty'],
        question_details['question_id'],
        question_details['question'],
        question_details['test_case'],
        question_details['title'],
    )
    output_path.mkdir(parents=True, exist_ok=True)
    file_name = f'{title.lower().replace(" ", "_").replace("-", "_")}.py'
    output_path = output_path / file_name
    content = f'"""\n{qid} - {difficulty} - {title}\n\n{question}"""\n\n'
    content += """def main():\n    ..."""
    content += "\n\nif __name__ == '__main__':\n    main()\n"
    content += '\n'.join(['    # d' for d in test_case.split('\n')])
    with output_path.open('w') as f:
        f.write(content)
    print(f'Created file for #{qid}: {title}')


def run(
        max_difficulty: Literal[1, 2, 3],
        min_difficulty: Literal[1, 2, 3],
        output_path: Path,
    ) -> None:
    all_questions = query_all_questions()
    question_slug = choose_a_valid_question(
        all_questions,
        max_difficulty,
        min_difficulty,
    )
    result = get_question_data(question_slug)
    question_details = parse_question_details(result)
    output_python_file(output_path, question_details)

