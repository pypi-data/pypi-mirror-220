from pathlib import Path
from bridgeobjects import load_pbn

from .. import next_card
from ..tests.utilities import get_board

BOARD_PATH = Path('tests', 'test_data', 'fourth_seat_defender.pbn')

boards = load_pbn(BOARD_PATH)[0].boards


def test_play_partners_suit():
    """Ensure notdiscard a winner."""
    board = get_board(boards, 0)
    assert next_card(board).name != 'QC'
