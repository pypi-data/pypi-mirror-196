from curses_toolkit.core import Cbreak


def actions(parent, exit_actions, loop_actions={}, initial_focus=0):
    parent.set_focus(initial_focus)
    parent.show()
    with Cbreak():
        while True:
            k = parent.pad.getkey()
            try:
                loop_actions[k](parent.focus, parent)
            except KeyError:
                pass
            try:
                exit_actions[k](parent.focus, parent)
                break
            except KeyError:
                pass
