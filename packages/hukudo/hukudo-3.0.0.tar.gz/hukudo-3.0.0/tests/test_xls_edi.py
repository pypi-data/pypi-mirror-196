from hukudo.xls.sheet import Sheet
from hukudo.xls.edi import EDI


def test_simple(ws):
    edi = EDI('B4')
    assert repr(edi) == "'B4'"
    ws[edi] = 'Hello'


def test_sheet(ws, table):
    sh = Sheet(ws)
    sh.add_table('B2', table)
