"""
Base de dados de FAQ (Perguntas Frequentes)
"""

import re
from difflib import SequenceMatcher

# Base de dados de FAQ
FAQ_DATABASE = [
    {
        "id": 1,
        "category": "tecnico",
        "question": "Como resolver problemas de conexão?",
        "answer": "Verifique sua conexão com a internet e tente novamente. Se o problema persistir, entre em contato com o suporte técnico.",
        "keywords": ["conexao", "internet", "rede", "conectar", "wifi"]
    },
    {
        "id": 2,
        "category": "conta",
        "question": "Como recuperar minha senha?",
        "answer": "Clique em 'Esqueci minha senha' na tela de login e siga as instruções enviadas para seu email.",
        "keywords": ["senha", "recuperar", "login", "esqueci", "email"]
    },
    {
        "id": 3,
        "category": "pagamento",
        "question": "Quais formas de pagamento são aceitas?",
        "answer": "Aceitamos cartões de crédito, débito, PIX e boleto bancário.",
        "keywords": ["pagamento", "cartao", "pix", "boleto", "credito", "debito"]
    },
    {
        "id": 4,
        "category": "produtos",
        "question": "Como fazer um pedido?",
        "answer": "Selecione os produtos desejados, adicione ao carrinho e finalize a compra seguindo as instruções.",
        "keywords": ["pedido", "comprar", "carrinho", "produto", "compra"]
    },
    {
        "id": 5,
        "category": "tecnico",
        "question": "O app não está funcionando, o que fazer?",
        "answer": "Tente fechar e abrir o aplicativo novamente. Se não resolver, desinstale e reinstale o app.",
        "keywords": ["app", "aplicativo", "funcionando", "erro", "bug", "reinstalar"]
    },
    {
        "id": 6,
        "category": "conta",
        "question": "Como alterar meus dados pessoais?",
        "answer": "Acesse 'Minha Conta' > 'Dados Pessoais' e faça as alterações necessárias.",
        "keywords": ["dados", "pessoais", "alterar", "conta", "perfil", "informacoes"]
    }
]

def search_faq(query, max_results=3):
    """
    Busca na FAQ baseado na query do usuário
    """
    if not query or len(query.strip()) < 2:
        return []

    query_lower = query.lower()
    results = []

    for faq in FAQ_DATABASE:
        score = 0

        # Busca por palavras-chave
        for keyword in faq['keywords']:
            if keyword in query_lower:
                score += 10

        # Busca na pergunta
        if query_lower in faq['question'].lower():
            score += 15

        # Busca na resposta
        if query_lower in faq['answer'].lower():
            score += 5

        # Busca por similaridade usando SequenceMatcher
        question_similarity = SequenceMatcher(None, query_lower, faq['question'].lower()).ratio()
        if question_similarity > 0.3:
            score += int(question_similarity * 10)

        if score > 0:
            results.append({
                'faq': faq,
                'score': score
            })

    # Ordenar por score (maior primeiro)
    results.sort(key=lambda x: x['score'], reverse=True)

    # Retornar apenas os FAQs, limitando ao máximo de resultados
    return [result['faq'] for result in results[:max_results]]

def get_faq_by_category(category):
    """
    Retorna FAQs de uma categoria específica
    """
    return [faq for faq in FAQ_DATABASE if faq['category'].lower() == category.lower()]

def get_all_categories():
    """
    Retorna todas as categorias disponíveis
    """
    categories = set()
    for faq in FAQ_DATABASE:
        categories.add(faq['category'])
    return list(categories)

def get_faq_by_id(faq_id):
    """
    Retorna FAQ específico por ID
    """
    for faq in FAQ_DATABASE:
        if faq['id'] == faq_id:
            return faq
    return None

def add_faq(category, question, answer, keywords=None):
    """
    Adiciona nova FAQ à base de dados
    """
    new_id = max([faq['id'] for faq in FAQ_DATABASE]) + 1 if FAQ_DATABASE else 1

    new_faq = {
        "id": new_id,
        "category": category,
        "question": question,
        "answer": answer,
        "keywords": keywords or []
    }

    FAQ_DATABASE.append(new_faq)
    return new_faq

def update_faq(faq_id, category=None, question=None, answer=None, keywords=None):
    """
    Atualiza FAQ existente
    """
    for i, faq in enumerate(FAQ_DATABASE):
        if faq['id'] == faq_id:
            if category:
                FAQ_DATABASE[i]['category'] = category
            if question:
                FAQ_DATABASE[i]['question'] = question
            if answer:
                FAQ_DATABASE[i]['answer'] = answer
            if keywords is not None:
                FAQ_DATABASE[i]['keywords'] = keywords
            return FAQ_DATABASE[i]
    return None

def delete_faq(faq_id):
    """
    Remove FAQ da base de dados
    """
    for i, faq in enumerate(FAQ_DATABASE):
        if faq['id'] == faq_id:
            return FAQ_DATABASE.pop(i)
    return None