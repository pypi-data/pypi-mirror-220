from pathlib import Path
from bridgeobjects import load_pbn

from .. import next_card
from ..tests.utilities import get_board

BOARD_PATH = Path('tests', 'test_data', 'third_seat_defender.pbn')

boards = load_pbn(BOARD_PATH)[0].boards


def test_play_partners_suit():
    """Return win if possible in _select_card_based_on_position."""
    board = get_board(boards, 0)
    assert next_card(board).name == 'AH'


def test_play_high_card():
    """Return highest card in _play_high_card."""
    board = get_board(boards, 1)
    print(board.tricks)
    assert next_card(board).name == 'TS'


def test_dont_play_high_card_if_partner_played_higher():
    """Do Not return highest card in _play_high_card."""
    board = get_board(boards, 2)
    assert next_card(board).name != 'KS'


def test_all_winners_in_long_suit():
    # Play winner if all winners
    board = get_board(boards, 3)
    assert next_card(board).name == 'KH'
