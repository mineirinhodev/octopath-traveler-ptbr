"""Leitor / gravador de arquivos .pak do Unreal Engine 4 (versão 4, zlib, sem criptografia)."""
import hashlib, struct, zlib

MAGIC = 0x5A6F12E1


def _rstr(b, p):
    n, = struct.unpack_from('<i', b, p)
    p += 4
    if n < 0:
        return b[p:p - 2 * n].decode('utf-16le').rstrip('\0'), p - 2 * n
    return b[p:p + n].rstrip(b'\0').decode('latin1'), p + n


def fstring(s):
    if s == '':
        return struct.pack('<i', 0)
    try:
        b = s.encode('ascii')
        return struct.pack('<i', len(b) + 1) + b + b'\0'
    except UnicodeEncodeError:
        return struct.pack('<i', -(len(s) + 1)) + s.encode('utf-16le') + b'\0\0'


class Pak:
    def __init__(self, path, base=0, size=None):
        self.f = open(path, 'rb')
        self.base = base
        if size is None:
            self.f.seek(0, 2)
            size = self.f.tell()
        self.f.seek(base + size - 44)
        magic, ver, ioff, isz = struct.unpack('<IIQQ', self.f.read(24))
        if magic != MAGIC or ver != 4:
            raise SystemExit(f'{path}: pak não reconhecido (magic {magic:#x}, versão {ver})')
        self.f.seek(base + ioff)
        b = self.f.read(isz)
        _, p = _rstr(b, 0)
        n, = struct.unpack_from('<i', b, p)
        p += 4
        self.entries = {}
        for _ in range(n):
            name, p = _rstr(b, p)
            off, csz, usz, cm = struct.unpack_from('<QQQI', b, p)
            p += 48
            blocks = []
            if cm:
                nb, = struct.unpack_from('<I', b, p)
                p += 4
                for i in range(nb):
                    blocks.append(struct.unpack_from('<QQ', b, p))
                    p += 16
            enc, = struct.unpack_from('<B', b, p)
            p += 5
            if enc:
                raise SystemExit(f'{name}: entrada criptografada')
            self.entries[name] = (off, usz, cm, blocks)

    def read(self, name):
        if name not in self.entries:
            raise SystemExit(f'não encontrei {name} no pak')
        off, usz, cm, blocks = self.entries[name]
        if cm == 0:
            self.f.seek(self.base + off + 53)
            return self.f.read(usz)
        d = b''
        for s, e in blocks:
            self.f.seek(self.base + s)
            d += zlib.decompress(self.f.read(e - s))
        assert len(d) == usz
        return d


def _record(off, data):
    return (struct.pack('<qqqi', off, len(data), len(data), 0) + hashlib.sha1(data).digest()
            + struct.pack('<BI', 0, 0))


def write(files, dst):
    """Grava um pak sem compressão com a lista [(nome, bytes)]."""
    body = b''
    idx = fstring('../../../') + struct.pack('<i', len(files))
    for name, data in files:
        idx += fstring(name) + _record(len(body), data)
        body += _record(0, data) + data
    foot = struct.pack('<IIqq', MAGIC, 4, len(body), len(idx)) + hashlib.sha1(idx).digest()
    with open(dst, 'wb') as f:
        f.write(body + idx + foot)
