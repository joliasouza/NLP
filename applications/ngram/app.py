import re
from collections import Counter, defaultdict
import streamlit as st

# Função para carregar o corpus
def load_corpus(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

corpus = load_corpus('harry_potter.txt')

# Pré-processamento
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-zà-ú0-9\s]', ' ', text)
    tokens = text.split()
    return tokens

tokens = preprocess(corpus)

# Interface Streamlit
st.title("Gerador de Frases com N-grams\n(Harry Potter Corpus)")

# Configuração do N-gram
n_size = st.slider("Tamanho do contexto (N-gram):", 2, 5, 2)
N = n_size

# Gera os n-grams
@st.cache_data
def get_ngram_counts(tokens, n):
    n_grams = [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]
    return Counter(n_grams)

n_gram_counts = get_ngram_counts(tokens, N)

# Função para prever a próxima palavra
def predict_next_word(context, n_gram_counts, n):
    context = tuple(context[-(n-1):]) if n > 1 else tuple()
    candidates = defaultdict(int)
    
    for gram, count in n_gram_counts.items():
        if gram[:-1] == context:
            candidates[gram[-1]] += count
    
    if candidates:
        total = sum(candidates.values())
        return sorted(((word, count/total) for word, count in candidates.items()), 
                      key=lambda x: x[1], reverse=True)
    else:
        if len(context) > 1:
            return predict_next_word(context[1:], n_gram_counts, n-1)
        else:
            return None

# Função para completar a frase
def complete_sentence(seed, num_words=10, show_probs=False):
    current_context = seed.copy()
    completed = []
    probabilities = []
    all_predictions = []  # Armazenará todas as previsões para cada passo
    
    for _ in range(num_words):
        predictions = predict_next_word(current_context, n_gram_counts, N)
        
        if not predictions:
            break
        
        # Armazena todas as previsões para este passo
        all_predictions.append(predictions)
        
        # Pega a palavra mais provável
        next_word = predictions[0][0]
        completed.append(next_word)
        probabilities.append(predictions[0][1])
        
        # Atualiza o contexto
        if len(current_context) >= N-1:
            current_context = current_context[-(N-1):] + [next_word]
        else:
            current_context.append(next_word)
    
    if show_probs:
        return ' '.join(completed), probabilities, all_predictions
    else:
        return ' '.join(completed)

# Entrada do usuário
entrada = st.text_input("Digite o início de uma frase:")

num_words=10

if entrada:
    palavras = entrada.strip().split()
    
    if palavras:
        # Modifique esta linha para pegar também all_predictions
        completacao, probs, all_predictions = complete_sentence([w.lower() for w in palavras], num_words, show_probs=True)
        
        st.subheader("Frase gerada:")
        st.write(f"**{entrada} {completacao}**")
        
        st.subheader("Detalhes das previsões:")
        
        # Mostra o processo de previsão usando all_predictions
        current_context = [w.lower() for w in palavras][-(N-1):]
        for i in range(min(num_words, len(probs))):
            predictions = all_predictions[i]  # Usa as previsões já calculadas
        
            st.write(f"Passo {i+1}:")
            st.write(f"P({predictions[0][0]} | {' '.join(current_context)}) = {probs[i]:.2%}")
        
            # Mostra alternativas (top 5)
            if len(predictions) > 1:
                st.write("Alternativas:")
                for j, (word, prob) in enumerate(predictions[:5], 1):
                    st.write(f"{j}. {word} (prob: {prob:.2%})")
        
            # Atualiza o contexto para a próxima iteração
            current_context = (current_context + [predictions[0][0]])[-(N-1):]
