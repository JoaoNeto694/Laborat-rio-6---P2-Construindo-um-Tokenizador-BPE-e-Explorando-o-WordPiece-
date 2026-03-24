# Laboratório 6 - P2: Construindo um Tokenizador BPE e Explorando o WordPiece 

Implementação do algoritmo Byte Pair Encoding (BPE) do zero e exploração do tokenizador WordPiece multilíngue do BERT via Hugging Face.

---

## Pré-requisitos

- Python 3.8+
- Hugging Face `transformers`

Instale as dependências com:

```bash
pip install transformers
```

---

## Como rodar

```bash
python lab6_bpe.py
```

---

## O que o código faz

### Componentes implementados

| Componente | Descrição |
|---|---|
| `get_stats(vocab)` | Varre o corpus e retorna a frequência de todos os pares de símbolos adjacentes |
| `merge_vocab(pair, v_in)` | Recebe o par mais frequente e retorna o vocabulário com todas as ocorrências desse par fundidas |
| Loop de treinamento | Executa `get_stats` + `merge_vocab` por 5 iterações, imprimindo o par fundido e o estado do vocabulário a cada rodada |
| Tarefa 3 — WordPiece | Carrega o `bert-base-multilingual-cased` e tokeniza uma frase de teste com o método `.tokenize()` |

### Fluxo de execução

**1. Motor de frequências (Tarefa 1)**
O corpus é representado como um dicionário Python onde as chaves são palavras separadas em caracteres (com símbolo `</w>` ao final) e os valores são suas frequências. A função `get_stats` percorre cada palavra, itera sobre os pares adjacentes e acumula a contagem ponderada pela frequência da palavra.

**2. Loop de fusão (Tarefa 2)**
A cada iteração, o par com maior frequência é identificado via `max(stats, key=stats.get)` e passado para `merge_vocab`, que usa expressão regular para substituir todas as ocorrências isoladas daquele par pela versão concatenada. O processo é repetido por K=5 rodadas.

**3. Integração com WordPiece (Tarefa 3)**
O tokenizador multilíngue do BERT é instanciado via `AutoTokenizer.from_pretrained` e aplicado sobre a frase de teste, demonstrando o particionamento morfológico em sub-palavras.

---

## Configuração padrão

```python
vocab = {
    'l o w </w>': 5,
    'l o w e r </w>': 2,
    'n e w e s t </w>': 6,
    'w i d e s t </w>': 3
}

K = 5  # Número de iterações de fusão
```

---

## Saída esperada

**Tarefa 1 — validação do par mais frequente:**
```
=== Tarefa 1: Frequências dos pares ===
Frequência do par ('e', 's'): 9
```

**Tarefa 2 — fusões ao longo das 5 iterações:**
```
=== Tarefa 2: Loop de Fusão (5 iterações) ===
Iteração 1: par fundido = ('e', 's')
  vocab = {'l o w </w>': 5, 'l o w e r </w>': 2, 'n e w es t </w>': 6, 'w i d es t </w>': 3}
Iteração 2: par fundido = ('es', 't')
  vocab = {'l o w </w>': 5, 'l o w e r </w>': 2, 'n e w est </w>': 6, 'w i d est </w>': 3}
Iteração 3: par fundido = ('est', '</w>')
  vocab = {'l o w </w>': 5, 'l o w e r </w>': 2, 'n e w est</w>': 6, 'w i d est</w>': 3}
Iteração 4: par fundido = ('l', 'o')
  vocab = {'lo w </w>': 5, 'lo w e r </w>': 2, 'n e w est</w>': 6, 'w i d est</w>': 3}
Iteração 5: par fundido = ('lo', 'w')
  vocab = {'low </w>': 5, 'low e r </w>': 2, 'n e w est</w>': 6, 'w i d est</w>': 3}
```

**Tarefa 3 — tokenização WordPiece:**
```
=== Tarefa 3: WordPiece com BERT Multilingual ===
Frase: Os hiper-parâmetros do transformer são inconstitucionalmente difíceis de ajustar.
Tokens: ['Os', 'hip', '##er', '-', 'par', '##âm', '##etros', 'do', 'transform', '##er',
         'são', 'in', '##cons', '##tit', '##uc', '##ional', '##mente', 'di', '##f',
         '##í', '##cei', '##s', 'de', 'aj', '##usta', '##r', '.']
```

---

## O que significa o `##` nos tokens do WordPiece

O prefixo `##` indica que aquele token é uma **continuação** de uma palavra — ou seja, ele não ocorre no início, mas sim no meio ou no fim. Por exemplo, `inconstitucionalmente` é dividida em `in` + `##cons` + `##tit` + `##uc` + `##ional` + `##mente`: apenas `in` é o token de início; todos os demais recebem `##` para sinalizar que são sufixos do mesmo item lexical.

Esse mecanismo impede o **travamento por vocabulário desconhecido** (`[UNK]`): em vez de descartar uma palavra inteira que não está no vocabulário, o tokenizador a decompõe em pedaços menores que ele conhece. Como os sub-tokens são unidades recorrentes na língua (raízes, prefixos, sufixos), o modelo consegue processar palavras novas, compostas ou raras sem perder a informação semântica embutida em sua morfologia.

---

## Uso de IA generativa

- A função `merge_vocab` foi gerada pela IA generativa.
- Estilização deste README.
