"""Acesso aos arquivos do RomFS: uma pasta extraída ou a imagem romfs.img (DMROMFS1) do NX Library."""
import os, struct


class RomFS:
    def __init__(self, path):
        self.path = path
        self.files = None
        if os.path.isdir(path):
            return
        with open(path, 'rb') as f:
            magic, ioff, isz, n = struct.unpack('<8sQQQ', f.read(0x20))
            if magic != b'DMROMFS1':
                raise SystemExit(f'{path}: não é uma pasta nem uma imagem DMROMFS1')
            f.seek(ioff)
            idx = f.read(isz)
        names = idx[n * 24:]
        ents = []
        for i in range(n):
            a, b, no, nl, isfile = struct.unpack_from('<QQIHH', idx, i * 24)
            ents.append((a, b, names[no:no + nl].decode(), isfile))
        self.files = {}

        def walk(i, prefix):
            a, b, name, isfile = ents[i]
            p = prefix + name
            if isfile:
                self.files[p] = (a, b)
            else:
                for c in range(a, a + b):
                    walk(c, p + '/' if p else '')
        walk(0, '')

    def locate(self, rel):
        """(arquivo no disco, deslocamento, tamanho) de um arquivo do RomFS."""
        if self.files is None:
            p = os.path.join(self.path, rel)
            if not os.path.isfile(p):
                raise SystemExit(f'não encontrei {rel} em {self.path}')
            return p, 0, os.path.getsize(p)
        if rel not in self.files:
            raise SystemExit(f'não encontrei {rel} em {self.path}')
        off, size = self.files[rel]
        return self.path, off, size
