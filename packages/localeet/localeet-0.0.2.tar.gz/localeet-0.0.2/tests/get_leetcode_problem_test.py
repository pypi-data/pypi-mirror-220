from pathlib import Path

from localeet.get_leetcode_problem import (
    choose_a_valid_question,
    get_question_data,
    output_python_file,
    parse_question_details,
    query_all_questions,
)


def test_query_all_questions(any_int):
    """Test that query for question list works"""
    result = query_all_questions()
    assert len(result) >= 2787  # assuming number never goes down..
    assert result[-1] == {  # assuming order never changes...
        'difficulty': {'level': 1},
        'frequency': 0,
        'is_favor': False,
        'paid_only': False,
        'progress': 0,
        'stat': {
            'frontend_question_id': 1,
            'is_new_question': False,
            'question__article__has_video_solution': True,
            'question__article__live': True,
            'question__article__slug': 'two-sum',
            'question__hide': False,
            'question__title': 'Two Sum',
            'question__title_slug': 'two-sum',
            'question_id': 1,
            'total_acs': any_int,
            'total_submitted': any_int,
        },
        'status': None,
    }


def test_choose_a_valid_question():
    result = choose_a_valid_question(query_all_questions(), 1, 1)
    assert isinstance(result, str)


def test_get_question_data(
        two_sum_details_json,
        any_int,
        any_json_str,
        any_str,
    ):
    two_sum_details_json['data']['question'].update({
        'dislikes': any_int,
        'judgeType': any_str,
        'likes': any_int,
        'stats': any_json_str,
    })
    assert get_question_data('two-sum') == two_sum_details_json


def test_parse_question_details(two_sum_details_json, two_sum_essentials):
    assert parse_question_details(two_sum_details_json) == two_sum_essentials


def test_output_python_file(two_sum_essentials, sample_two_sum_python_file):
    path = Path('.')
    new_file = path / 'two_sum.py'
    output_python_file(path, two_sum_essentials)
    with new_file.open() as f:
        test_file = f.read()
    assert test_file == sample_two_sum_python_file
    new_file.unlink()
