from curses_toolkit.core import Cbreak, NoDelay


def test_cbreak(core_curses):
    with Cbreak():
        core_curses.cbreak.assert_called_once_with()
    core_curses.nocbreak.assert_called_once_with()


def test_nodelay(core_curses):
    with NoDelay(5):
        core_curses.nodelay.assert_called_once_with(5)
    core_curses.nocbreak.assert_called_once_with()
