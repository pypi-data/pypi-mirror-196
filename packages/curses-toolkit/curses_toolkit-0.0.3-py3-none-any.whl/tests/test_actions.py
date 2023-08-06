from curses_toolkit import actions


def test_list_exit_actions(mocker, list_pad, core_curses, list_days):
    list_pad.getkey.return_value = 'd'
    action_sink = mocker.MagicMock()
    actions(list_days, {
        'd': lambda i, ls: action_sink.action_d(i, ls),
        })
    action_sink.action_d.assert_called_once_with(0, list_days)


def test_list_loop_actions(mocker, list_pad, core_curses, list_days):
    list_pad.getkey.side_effect = ['k', 'k', 'd', 'j']
    action_sink = mocker.MagicMock()
    actions(list_days,
            {
                'd': lambda i, ls: action_sink.action_d(i, ls),
                },
            loop_actions={
                'j': lambda i, ls: action_sink.action_j(i, ls),
                'k': lambda i, ls: action_sink.action_k(i, ls),
                })
    action_sink.action_j.assert_not_called()
    assert 2 == len(action_sink.action_k.mock_calls)
    action_sink.action_d.assert_called_once_with(0, list_days)
