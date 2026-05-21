# Passo a passo das altera\u00e7\u00f5es - 2026-05-21

1. Corrigi o padr\u00e3o do `.gitignore` para ignorar `meu_venv/` corretamente.
2. Removi o diret\u00f3rio `meu_venv` do \u00edndice do Git para que ele pare de ir para o remoto sem apagar os arquivos locais.
3. Separei a l\u00f3gica principal em m\u00f3dulos de dominio:
   - `src/core/models.py` para os objetos de dados.
   - `src/core/profiles.py` para classifica\u00e7\u00e3o, normaliza\u00e7\u00e3o e parsing.
   - `src/core/excel_writer.py` para escrita e limpeza da planilha.
   - `src/core/workflow.py` para orquestra\u00e7\u00e3o do fluxo.
4. Reescrevi a GUI para consumir o servi\u00e7o novo e exibir barra de progresso.
5. Ajustei a regra de agrupamento para que perfis com a mesma chave normalizada, incluindo o caso de perfil duplo + normal da mesma medida, somem suas metragens antes da grava\u00e7\u00e3o.
6. Mantive `src/processor.py` como camada de compatibilidade para n\u00e3o quebrar chamadas antigas.
7. Criei esta documenta\u00e7\u00e3o de apoio em Markdown dentro de `docs contexto`.
