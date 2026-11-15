# OCTOPATH TRAVELER — Tradução PT-BR (não oficial)

Tradução dos textos de **OCTOPATH TRAVELER** (Nintendo Switch, title ID `010057D006492000`) para
**português do Brasil**. O jogo não tem português; a tradução entra no lugar do texto em inglês.

- Interface, menus, batalha, habilidades, itens, tutoriais, diário e os diálogos das oito histórias, das histórias
  paralelas e dos NPCs.
- 40.089 textos em 91 arquivos (cerca de 339 mil palavras em português).
- Vozes, vídeos e textos desenhados em imagens continuam como no original.

> **Aviso:** a tradução **ainda não foi revisada linha a linha nem conferida na tela do jogo**. Espere
> inconsistências, frases estranhas e linhas que não cabem na caixa de texto. Correções são bem-vindas: veja
> [Como contribuir](#como-contribuir).

## O que há neste repositório

Este repositório **não contém arquivos do jogo**. Ele guarda só o texto traduzido e os scripts que o aplicam sobre o
seu próprio dump:

```
texto/      texto em português, em JSON, separado por tabela do jogo
tools/      scripts em Python para montar o mod e exportar texto
```

As tabelas de texto do jogo (`.uasset` / `.uexp`) também carregam dados originais que não são texto, por isso o mod
já montado não é distribuído aqui.

## Como montar o mod

Você precisa do Python 3 (sem dependências) e do RomFS do seu próprio jogo, extraído do seu dump.

Rode, apontando para a raiz do RomFS (a pasta que contém `Kingship/Content/Paks/Kingship-Switch.pak`) ou, no
NX Library, direto para o `romfs.img` do jogo:

```
python3 tools/build.py "caminho/para/romfs" "Traducao PT-BR"
python3 tools/build.py "/caminho/OCTOPATH TRAVELER.app/Contents/Resources/romfs.img" "Traducao PT-BR"
```

O resultado é uma pasta de mod pronta, com um único arquivo de uns 15 MB:

```
Traducao PT-BR/
└── romfs/
    └── Kingship/Content/Paks/Kingship-Switch_0_P.pak
```

Textos do jogo que não tiverem tradução (por exemplo, numa versão mais nova) ficam em inglês e o script avisa
quantos são.

## Instalação

Em qualquer caso, **deixe o idioma do jogo em inglês**: o português aparece no lugar dele.

### NX Library (Mac)

1. Copie a pasta `Traducao PT-BR` para
   `/Applications/NxNative_Data/AppSupport/010057D006492000/mods/`
2. Abra o NX Library, entre em OCTOPATH TRAVELER → **Mods** e ligue `Traducao PT-BR`.
3. Inicie o jogo.

### Switch com Atmosphère

Copie o conteúdo da pasta `romfs` do mod para o cartão SD em

```
atmosphere/contents/010057D006492000/romfs/
```

Não testado.

### Outros emuladores

Emuladores que aceitam mods no formato `romfs` costumam ter uma pasta de mods por jogo: abra-a pelo menu do
emulador e copie a pasta `Traducao PT-BR` inteira para lá. Não testado.

### Desinstalar

Desligue o mod ou apague a pasta. Nada no jogo nem no save é alterado.

## Escolhas de tradução

- Nomes de personagens, cidades e deuses ficam como no original (Olberic, Tressa, Cyrus, Primrose, H'aanit,
  Therion, Ophilia, Alfyn, Orsterra, Atlasdam, Aelfric, Galdera…).
- Regiões, classes, habilidades, itens e termos do sistema são traduzidos:

  | Inglês | Português |
  |---|---|
  | Merchant / Thief / Warrior / Hunter | Mercador(a) / Ladrão / Guerreiro / Caçador(a) |
  | Cleric / Dancer / Scholar / Apothecary | Clérigo(a) / Dançarina / Erudito / Boticário |
  | Path Action | Ação de Caminho |
  | Boost / Break | Impulso / Quebra |
  | Frostlands / Flatlands / Coastlands / Highlands | Terras Geladas / Planícies / Terras Costeiras / Terras Altas |
  | Sunlands / Riverlands / Cliftlands / Woodlands | Terras do Sol / Terras Fluviais / Terras dos Penhascos / Terras Florestais |
  | leaves (moeda) | folhas |

- H'aanit e sua gente, que falam inglês arcaico no original, falam com "tu" / "vós" e construções antigas.
- As siglas HP, SP, BP, JP e EXP ficam como estão.

## Limitações conhecidas

- A única conferência dentro do jogo foi de carregamento: no NX Library, o jogo abre o arquivo do mod e lê as duas
  tabelas inteiras. O texto não foi olhado na tela.
- A tela de Game Over continua em inglês: o jogo monta o título com pedaços de letras.
- Textos que são imagens (logotipo, "BREAK", "MISS" e parecidos) não mudam.
- As falas são quebradas pelo script em linhas de até 50 caracteres; em menus apertados, um texto pode ficar mais
  largo que o espaço.
- O gênero de quem fala ou de quem ouve foi deduzido pelo contexto e pode estar errado em algumas falas.
- Instalação em Atmosphère e em outros emuladores não foi testada.

## Como contribuir

Achou um erro? Abra uma [issue](../../issues) com a frase como aparece no jogo (uma captura de tela ajuda) ou mande
um pull request.

A tradução fica em `texto/GameText/` (menus, batalha, itens, diário) e `texto/TalkData/` (falas). Cada arquivo é um
objeto `{"LINHA": "texto em português"}`, em que a linha é o nome que o próprio jogo dá àquele texto; os arquivos
agrupam as linhas pelo começo do nome (`TX_MS` história principal, `TX_SS` histórias paralelas, `TX_NP` NPCs,
`TX_PC` conversas do grupo, `BT` batalha…). Para corrigir uma frase, procure-a nesses arquivos e edite o valor,
mantendo:

- as variáveis `{0}`, `{1}`… e os símbolos (`⑳` é a moeda);
- as marcações `<span style="italic">…</>` e `<br>`;
- as quebras de linha que já existirem (`\n`, ou os dois caracteres `\\n` nos textos de menu). Não acrescente
  quebras nas falas: o script cuida disso.

## Scripts

| Script | Função |
|---|---|
| `tools/build.py` | aplica `texto/` sobre as tabelas do seu dump e grava a pasta do mod |
| `tools/extract.py` | exporta o texto do seu dump para JSON, no mesmo formato de `texto/` (aceita o idioma: `EN`, `JA`, `FR`, `DE`, `ES`, `IT`) |
| `tools/tabela.py` | leitor / gravador do texto das tabelas (`.uasset` / `.uexp`) |
| `tools/pak.py` | leitor / gravador de arquivos `.pak` do Unreal Engine 4 |
| `tools/romfs.py` | acesso ao RomFS: pasta extraída ou imagem `romfs.img` do NX Library |

### Detalhe técnico

O jogo usa o Unreal Engine 4.18. O texto está em duas DataTables dentro de `Kingship-Switch.pak`:
`GameText/Database/GameTextEN` (uma propriedade de texto por linha) e `Talk/Database/TalkData_EN` (uma fala por
linha, com tipo de balão e nome de quem fala). O `build.py` troca só as cadeias de texto, casando-as pelo nome da
linha, ajusta os tamanhos no `.uasset` e grava as duas tabelas num pak de patch sem compressão
(`Kingship-Switch_0_P.pak`), que o jogo carrega por cima do original. O pak do jogo não é modificado.

## Aviso legal

Projeto de fã, sem fins lucrativos, sem vínculo com a Square Enix nem com a Nintendo. OCTOPATH TRAVELER é marca e
propriedade de seus respectivos donos. Este repositório não inclui o jogo nem seus arquivos originais e só funciona
com uma cópia sua, obtida legalmente. Os scripts em `tools/` estão sob a licença MIT (veja [`LICENSE`](LICENSE)).
