# Contribuindo para o mtcli-rsi
  
Obrigado por considerar contribuir com este projeto! Abaixo estão instruções para configurar o ambiente de desenvolvimento, executar os testes e entender a estrutura do projeto.
  
---
  
## Instalação para desenvolvimento
  
Clone o repositório e instale as dependências com o Poetry:
  
```bash
git clone https://github.com/vfranca/mtcli-rsi.git
cd mtcli-rsi
poetry install
```
  
---
  
## Executando os testes
  
Para rodar todos os testes automatizados:
  
```bash
poetry run pytest
```
  
---
  
## Estrutura do Projeto
  
- plugin.py: Comando CLI com Click.
- rsi.py: Lógica de cálculo e formatação do RSI.
- tests/: Testes automatizados com pytest.
- mtcli/: Funções auxiliares (como conecta.py, logger.py, etc.).
  
---
  
## Boas práticas
  
- Escreva testes para cada nova funcionalidade.
- Use docstrings para documentar funções e módulos.
- Faça commits claros e descritivos.
- Siga o padrão e estilo do projeto para manter a consistência.
- Sempre que possível, atualize o README ou docs relevantes.
  
---
  
## Publicação (mantenedores)
  
Para publicar uma nova versão no PyPI:
  
```bash
poetry build
poetry publish
```
  
---
  
Fique à vontade para abrir issues ou enviar pull requests. Toda ajuda é bem-vinda!
