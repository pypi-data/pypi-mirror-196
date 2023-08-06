from curses_toolkit.core import BlockingInput


def selector(parent):
    selected = False
    focus = 0
    with BlockingInput():
        while not selected:
            focus = parent.set_focus(focus)
            parent.show()
            match parent.pad.getkey():
                case 'j':
                    focus += 1
                case 'k':
                    focus -= 1
                case '\n':
                    selected = True
                case 'x':
                    focus = None
                    break
    parent.set_no_focus()
    parent.show()
    return focus
