import re

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


# Tarefa 2: O Loop de Fusão
# Função que recebe o par mais frequente extraído no Passo 1 (ex: ('e', 's')) e o dicionário do 
# vocabulário atual. 
def merge_vocab(pair, v_in):
    v_out = {}
    bigram = ' '.join(pair)
    replacement = ''.join(pair)
    for word in v_in:
        # Substitui o par adjacente pela versão fundida
        new_word = re.sub(r'(?<!\S)' + re.escape(bigram) + r'(?!\S)', replacement, word)
        v_out[new_word] = v_in[word]
    return v_out

# Loop Principal de Treinamento do Tokenizador
for i in range(5):
    stats = get_stats(vocab)
    best_pair = max(stats, key=stats.get)
    vocab = merge_vocab(best_pair, vocab)
    print(f"Iteração {i + 1}: par fundido = {best_pair}")
    print(f"  vocab = {vocab}")
