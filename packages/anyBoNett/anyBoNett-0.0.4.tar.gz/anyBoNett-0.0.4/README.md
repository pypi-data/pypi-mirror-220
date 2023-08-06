# Minha Biblioteca

## Descrição
Minha Biblioteca é uma ferramenta poderosa para fazer coisas incríveis na internet, como : pesquisas.

## Instalação
Para instalar a biblioteca, execute o seguinte comando: "pip install anyBoNett==0.0.4"


## Uso
Aqui está um exemplo simples de como usar a biblioteca:

```python
import anybonett.NET as anybo

print(anybo.search_wikipedia("Einstein", "pt", 3)) # O primero parametro e para a pesquisa, a segunda é o idioma e o ultimo é quantas linhas

anybo.search_google("hello google") # Vai fazer uma pesquisa direta para google, pesquisando "hello google"

anybo.search_youtube("hello youtube") # Vai fazer uma pesquisa direta para youtube, pesquisando "hello youtube"




