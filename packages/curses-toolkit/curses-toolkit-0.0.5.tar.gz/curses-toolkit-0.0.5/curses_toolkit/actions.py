from curses_toolkit.core import Cbreak


def actions(parent, exit_actions, loop_actions={}, initial_focus=0):
    ret = None
    parent.set_focus(initial_focus)
    with Cbreak():
        while True:
            parent.show()
            k = parent.pad.getkey()
            try:
                loop_actions[k](parent.focus, parent)
            except KeyError:
                pass
            try:
                ret = exit_actions[k](parent.focus, parent)
                break
            except KeyError:
                pass
    parent.focus = None
    parent.show()
    return ret


KEYS_VIM_SELECT = {
        '\x1b': lambda i, ls: None,
        'x': lambda i, ls: None,
        '\n': lambda i, ls: i,
        }

KEYS_VIM_UP_DOWN = {
        'k': lambda i, ls: ls.set_focus(ls.focus - 1),
        'j': lambda i, ls: ls.set_focus(ls.focus + 1),
        }

# TODO: default actions dicts e.g. k & j for up & down
