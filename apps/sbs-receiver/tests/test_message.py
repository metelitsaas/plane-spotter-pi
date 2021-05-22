"""Test the Message class"""
from message import Message


def test__parse():
    """
    Test _parse function
    """
    assert Message._parse(b'MSG,4,5,211,4CA2D6,10057,2008/11/28,14:53:49.986,'
                          b'2008/11/28,14:58:51.153,,,408.3,146.4,,,64,,,,,') == [
               'MSG', '4', '5', '211', '4CA2D6', '10057', '2008/11/28', '14:53:49.986', '2008/11/28',
               '14:58:51.153', '', '', '408.3', '146.4', '', '', '64', '', '', '', '', ''
           ]
    assert len(Message._parse(b'MSG,4,5,211,4CA2D6,10057,2008/11/28,14:53:49.986,'
                              b'2008/11/28,14:58:51.153,,,408.3,146.4,,,64,,,,,')) == 22
    assert len(Message._parse(b'MSG,4,5,211,4CA2D6,10057,2008/11/28,14:53:49.986,'
                              b'2008/11/28,14:58:51.153,,,408.3,146.4,,,64,,,,,,')) == 0
    assert len(Message._parse(b'MSG,4,5,211,4CA2D6,10057,2008/11/28,14:53:49.986,'
                              b'2008/11/28,14:58:51.153,,,408.3,146.4,,,64,,,,')) == 0
    assert len(Message._parse(b'')) == 0


def test_message_type():
    """
    Test message_type property
    """
    assert Message(b'MSG,4,5,211,4CA2D6,10057,2008/11/28,14:53:49.986,'
                   b'2008/11/28,14:58:51.153,,,408.3,146.4,,,64,,,,,').message_type == 'MSG'
    assert Message(b'SEL,4,5,211,4CA2D6,10057,2008/11/28,14:53:49.986,'
                   b'2008/11/28,14:58:51.153,,,408.3,146.4,,,64,,,,,').message_type == 'SEL'
    assert Message(b'MS,4,5,211,4CA2D6,10057,2008/11/28,14:53:49.986,'
                   b'2008/11/28,14:58:51.153,,,408.3,146.4,,,64,,,,,').message_type is None


def test_transmission_type():
    """
    Test transmission_type property
    """
    assert Message(b'MSG,4,5,211,4CA2D6,10057,2008/11/28,14:53:49.986,'
                   b'2008/11/28,14:58:51.153,,,408.3,146.4,,,64,,,,,').transmission_type == 4
    assert Message(b'MSG,8,5,211,4CA2D6,10057,2008/11/28,14:53:49.986,'
                   b'2008/11/28,14:58:51.153,,,408.3,146.4,,,64,,,,,').transmission_type == 8
    assert Message(b'MSG').transmission_type is None
    assert Message(b'MSG,MSG,5,211,4CA2D6,10057,2008/11/28,14:53:49.986,'
                   b'2008/11/28,14:58:51.153,,,408.3,146.4,,,64,,,,,').transmission_type is None
