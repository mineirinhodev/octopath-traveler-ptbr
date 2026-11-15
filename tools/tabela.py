"""Leitura e troca do texto das DataTables de texto do jogo (pares .uasset / .uexp do UE 4.18)."""
import struct
from pak import fstring


def _rstr(b, p):
    n, = struct.unpack_from('<i', b, p)
    p += 4
    if n < 0:
        return b[p:p - 2 * n].decode('utf-16le')[:-1], p - 2 * n
    if n == 0:
        return '', p
    return b[p:p + n - 1].decode('latin1'), p + n


def _names(ua):
    p = 24 + struct.unpack_from('<I', ua, 20)[0] * 20 + 4
    _, p = _rstr(ua, p)
    _, count, off = struct.unpack_from('<Iii', ua, p)
    names = []
    for _ in range(count):
        s, off = _rstr(ua, off)
        off += 4
        names.append(s)
    return names, struct.unpack_from('<Iii', ua, p)[2]


def _walk(ua, ue):
    """Gera (linha, posição do tamanho da propriedade, tamanho, início, fim, texto) de cada texto."""
    names, _ = _names(ua)
    p = 0

    def name():
        nonlocal p
        i, num = struct.unpack_from('<II', ue, p)
        p += 8
        return names[i] + (f'_{num - 1}' if num else '')

    def props(row):
        nonlocal p
        while True:
            nm = name()
            if nm == 'None':
                return
            ty = name()
            szpos = p
            size, = struct.unpack_from('<i', ue, p)
            p += 8
            if ty == 'StructProperty':
                p += 24
            elif ty == 'BoolProperty':
                p += 1
            elif ty in ('ByteProperty', 'EnumProperty', 'ArrayProperty'):
                p += 8
            p += 1
            start = p
            if row is not None and nm == 'Text' and ty == 'TextProperty':
                if struct.unpack_from('<b', ue, p + 4)[0] == 0:
                    q = p + 5
                    _, q = _rstr(ue, q)
                    _, q = _rstr(ue, q)
                    s, e = _rstr(ue, q)
                    yield row, szpos, size, q, e, s
            elif row is not None and nm == 'Text' and ty == 'ArrayProperty':
                assert struct.unpack_from('<i', ue, p)[0] == 1
                s, e = _rstr(ue, p + 4)
                yield row, szpos, size, p + 4, e, s
            p = start + size

    yield from props(None)
    n, = struct.unpack_from('<i', ue, p + 4)
    p += 8
    for _ in range(n):
        yield from props(name())
    assert ue[p:] == b'\xc1\x83\x2a\x9e', 'fim inesperado da tabela'


def textos(ua, ue):
    """Lista [(linha, texto)] na ordem do arquivo."""
    return [(r, s) for r, _, _, _, _, s in _walk(ua, ue)]


def trocar(ua, ue, novo):
    """novo(linha, texto) -> texto novo ou None. Devolve (uasset, uexp, quantos textos mudaram)."""
    out, last, cnt = [], 0, 0
    for row, szpos, size, a, b, s in _walk(ua, ue):
        t = novo(row, s)
        if t is None or t == s:
            continue
        enc = fstring(t)
        out += [ue[last:szpos], struct.pack('<i', size + len(enc) - (b - a)), ue[szpos + 4:a], enc]
        last = b
        cnt += 1
    out.append(ue[last:])
    new = b''.join(out)
    ua = bytearray(ua)
    _, noff = _names(ua)
    # tamanho do export e início dos bulk data acompanham o novo tamanho do .uexp
    k = struct.pack('<qq', len(ue) - 4, len(ua))
    i = ua.find(k)
    assert i > 0 and ua.find(k, i + 1) < 0
    ua[i:i + 8] = struct.pack('<q', len(new) - 4)
    k = struct.pack('<q', len(ua) + len(ue) - 4)
    j = ua.find(k, 0, noff)
    assert j > 0 and ua.find(k, j + 1, noff) < 0
    ua[j:j + 8] = struct.pack('<q', len(ua) + len(new) - 4)
    return bytes(ua), new, cnt
