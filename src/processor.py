from src.core.workflow import MaterialAutomationService
from src.core.models import MaterialItem


_SERVICE = MaterialAutomationService()


def extrair_dados_word(caminho_arquivo_word):
    dados = _SERVICE.extrair_dados_word(caminho_arquivo_word)
    if not dados:
        return dados

    return [[item.descricao, item.aco, item.comprimento_m, item.peso_total] for item in dados]


def preencher_planilha_excel(caminho_planilha, dados_materiais):
    itens_convertidos: list[MaterialItem] = []

    for item in dados_materiais:
        if isinstance(item, MaterialItem):
            itens_convertidos.append(item)
            continue

        descricao, aco, comprimento_m, peso_total = item
        itens_convertidos.append(_SERVICE.parser.criar_item(descricao, aco, comprimento_m, peso_total))

    return _SERVICE.preencher_planilha_excel(caminho_planilha, itens_convertidos)


def processar_arquivo(caminho_arquivo_word, caminho_planilha, callback=None):
    return _SERVICE.processar(caminho_arquivo_word, caminho_planilha, callback=callback)