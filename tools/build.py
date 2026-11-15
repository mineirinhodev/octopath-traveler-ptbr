#!/usr/bin/env python3
"""Aplica texto/ sobre o seu dump e grava a pasta do mod.

uso: python3 tools/build.py <romfs.img ou pasta do RomFS> <pasta do mod>
"""
import os, re, sys
from comum import TABELAS, RAIZ, abrir, ler_texto, sem_quebra
import pak, tabela

LARGURA = 50   # caracteres por linha de uma fala
IT = '<span style="italic">'
TAG = re.compile(r'<[^>]*>')


def visivel(s):
    return len(TAG.sub('', s))


def italico_por_palavra(s):
    """Nas falas o jogo não quebra a linha dentro de um itálico: cada palavra leva a sua marcação."""
    return re.sub(re.escape(IT) + r'(.*?)</>',
                  lambda m: ' '.join(IT + w + '</>' for w in m.group(1).split(' ') if w), s)


def quebrar(s):
    out = []
    for trecho in s.split('\n'):
        linhas, cur = [], ''
        for w in re.split(r' (?![^<]*>)', trecho):
            if cur and visivel(cur) + 1 + visivel(w) > LARGURA:
                linhas.append(cur)
                cur = w
            else:
                cur = cur + ' ' + w if cur else w
        linhas.append(cur)
        out.append(' \n'.join(linhas))
    return '\n'.join(out)


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    jogo = abrir(sys.argv[1])
    arquivos = []
    for nome, caminho in TABELAS.items():
        caminho = caminho.format('EN')
        pt = ler_texto(os.path.join(RAIZ, nome))
        ua, ue = jogo.read(caminho + '.uasset'), jogo.read(caminho + '.uexp')
        faltam = []

        def novo(linha, s):
            if linha not in pt:
                if re.search('[A-Za-z]', s) and s != 'None':
                    faltam.append(linha)
                return None
            t = pt[linha]
            if nome != 'TalkData':
                return t
            t = italico_por_palavra(t)
            # textos que o original não quebra à mão (linhas longas) são quebrados pelo próprio jogo
            return t if max(visivel(l) for l in s.split('\n')) > 60 else quebrar(t)

        ua, ue, n = tabela.trocar(ua, ue, novo)
        print(f'{nome}: {n} textos trocados, {len(faltam)} sem tradução (ficam em inglês)')
        arquivos += [(caminho + '.uasset', ua), (caminho + '.uexp', ue)]
    destino = os.path.join(sys.argv[2], 'romfs', 'Kingship', 'Content', 'Paks')
    os.makedirs(destino, exist_ok=True)
    destino = os.path.join(destino, 'Kingship-Switch_0_P.pak')
    pak.write(arquivos, destino)
    print(destino)


if __name__ == '__main__':
    main()
