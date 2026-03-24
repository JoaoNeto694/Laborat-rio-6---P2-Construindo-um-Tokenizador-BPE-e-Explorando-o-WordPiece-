# Laboratório 6 - P2: Construindo um Tokenizador BPE e Explorando o WordPiece

# Tarefa 1: O Motor de Frequências
vocab = {
    'l o w </w>': 5,
    'l o w e r </w>': 2,
    'n e w e s t </w>': 6,
    'w i d e s t </w>': 3
}

# Recebe esse dicionário e retorna as frequências de todos os pares adjacentes de caracteres/símbolos. 
def get_stats(vocab):
    pairs = {}
    for word, freq in vocab.items():
        symbols = word.split()
        for i in range(len(symbols) - 1):
            pair = (symbols[i], symbols[i + 1])
            pairs[pair] = pairs.get(pair, 0) + freq
    return pairs

# Validação da Tarefa 1
# Resultado Esperado: Frequência do par ('e', 's'): 9
stats = get_stats(vocab)
print(f"Frequência do par ('e', 's'): {stats.get(('e', 's'), 0)}")
