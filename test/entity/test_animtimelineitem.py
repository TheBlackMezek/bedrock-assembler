from brockassemble.entity import AnimTimelineItem


def test_json_single_cmd():
    cmd = 'say Hi!'
    ati = AnimTimelineItem(commands=[cmd])
    assert ati.get_json() == cmd


def test_json_multi_cmd():
    cmd1 = 'say Hi!'
    cmd2 = 'say Bye!'
    cmds = [cmd1, cmd2]
    ati = AnimTimelineItem(commands=cmds)
    assert ati.get_json() == cmds


def test_add_cmd():
    cmd1 = 'say Hi!'
    cmd2 = 'say Bye!'
    cmds = [cmd1, cmd2]
    ati = AnimTimelineItem(commands=[cmd1])
    ati.add_command(cmd2)
    assert ati.get_json() == cmds


def test_add_cmds():
    cmd1 = 'say Hi!'
    cmd2 = 'say Bye!'
    cmd3 = 'say What is the air speed of an unladen swallow?'
    cmds = [cmd1, cmd2, cmd3]
    ati = AnimTimelineItem(commands=[cmd1])
    ati.add_commands([cmd2, cmd3])
    assert ati.get_json() == cmds


def test_init_trigger_time():
    test_value = 1.0
    ati = AnimTimelineItem(trigger_time=test_value)
    assert ati.trigger_time == test_value
