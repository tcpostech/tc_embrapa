# Tech Challenge 01 - Embrapa

### O problema

Você foi contratado(a) para uma consultoria e seu trabalho envolve analisar os dados de vitivinicultura da Embrapa, 
os quais estão disponíveis [aqui](http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01).

> **Aviso**: O link pode eventualmente sofrer instabilidade por se tratar do site do EMBRAPA. Caso isso ocorra, 
> por gentileza, tente novamente em alguns minutos.

A ideia do projeto é a criação de uma API pública de consulta nos dados do site nas respectivas abas:
- Produção.
- Processamento.
- Comercialização.
- Importação.
- Exportação.


A API vai servir para alimentar uma base de dados que futuramente será usada para um modelo de Machine Learning.

### Seus objetivos incluem:
- [x] Criar uma Rest API em Python que faça a consulta no site da Embrapa.
- [x] Sua API deve estar documentada.
- [x] É recomendável (não obrigatório) a escolha de um método de autenticação (JWT, por exemplo).
- [x] Criar um plano para fazer o deploy da API, desenhando a arquitetura do projeto desde a ingestão até a alimentação do modelo (aqui não é Tech Challenge necessário elaborar um modelo de ML, mas é preciso que vocês escolham um cenário interessante em que a API possa ser utilizada).
- [x] Fazer um MVP realizando o deploy com um link compartilhável e um repositório no GitHub.

---

### Requisitos para a utlização em ambiente local
- Faça uma cópia do arquivo **.env.text** e crie um arquivo **.env**.
- Preencha cada uma das variáveis de acordo com o seu ambiente de desenvolvimento.
- Crie um banco de dados e realize as migrations com o comando: ``alembic upgrade head``.
- Ao utilizar a aplicação em ambiente local, será possível visualizar a documentação pelo modelo [Swagger](http://127.0.0.1:8000/documentation/swagger) e [Redoc](http://127.0.0.1:8000/documentation/redoc). Variando o domínio de acordo com o ambiente que você estiver executando.
- Para utilizar a API responsável realizar um cadastro e em seguida se autenticar para que seja possível visualizar o conteúdo extraído do site da Embrapa.
- Antes de realizar qualquer modificação, instalar hook do *pre-commit* ``pre-commit install``.
- Para atualizar a documentação, basta atualizar este arquivo e em seguida utilizar o comando ``mkdocs build`` para que ele seja atualizado no diretório *site*.
- Para visualizar apenas a documentação, basta utilizar o comando: ``mkdocs serve``.
- Para executar o projeto em ambiente local, basta utilizar o comando: ``fastapi dev src/``.


### Principais bibliotecas para o desenvolvimento
- **Alembic:** Ferramenta de migração de banco de dados para SQLAlchemy, facilitando versionamento e atualização de esquemas.
- **Asyncpg:** Cliente PostgreSQL assíncrono eficiente e rápido, ideal para aplicações de alto desempenho.
- **Bcrypt:** Biblioteca de hashing de senhas segura, resistente a ataques de força bruta.
- **FastAPI:** Framework web moderno e rápido para APIs, baseado em Python e tipo hints.
- **Fastapi-Mail:** Biblioteca para envio de e-mails assíncronos com FastAPI e suporte a templates.
- **ItsDangerous:** Ferramenta para criar tokens seguros e assinar dados de forma confiável.
- **MkDocs:** Gera sites de documentação estática usando Markdown, simples e eficiente.
- **MkDocs Material:** Um tema elegante para MkDocs, baseado no Material Design, com recursos avançados.
- **Pre Commit:** Framework para gerenciamento de hooks Git, automatizando verificações antes de commits.
- **Pydantic:** Validação de dados poderosa baseada em Python, usando modelos e tipo hints.
- **Pydantic Settings:** Gerenciamento de configurações utilizando Pydantic, facilitando validação e carregamento de variáveis.
- **Pylint:** Ferramenta de análise de código Python que verifica padrões e boas práticas.
- **PyJWT:** Manipulação de tokens JWT para autenticação segura em aplicações web.
- **SQLModel:** Biblioteca para manipulação de bancos de dados usando Pydantic e SQLAlchemy de maneira intuitiva.

### Passos para o deploy utilizando o [Render](https://dashboard.render.com/)
- Configurar um banco de dados Postgres
- Executar a aplicação em ambiente local com a nova conexão da base de dados para atualizar todas as tabelas
- Configurar um novo Web Service
- Incluir todas as variáveis inclusas no arquivo **.env**

### Diagrama de fluxo

Esta seção apresenta uma forma simplificada de como funciona o fluxo de escrita e leitura.
```mermaid
flowchart TD
    A["Usuário"] <-- Acesso ao sistema e consulta de dados persistidos --> B["Sistema Interno"]
    B -- Busca os arquivos por HTTP --> C["Site Externo"]
    C -- Retorno dos dados em CSV --> B
    B <-- Salva e recupera dados no banco --> D["Banco de Dados"]
```

- Modelagem do banco de dados para os dados da Embrapa
```mermaid
erDiagram
    tb_users {
        UUID uid
        VARCHAR(255) first_name
        VARCHAR(255) last_name
        VARCHAR(255) username
        VARCHAR(255) email
        VARCHAR(255) password
        BOOLEAN is_verified
		TIMESTAMP created_at
		TIMESTAMP updated_at
    }
    
	tb_category ||--o{ tb_subcategory : references

	tb_category {
		UUID uid
		VARCHAR(255) category
		TIMESTAMP created_at
		TIMESTAMP updated_at
	}

	tb_subcategory {
		UUID uid
		VARCHAR(255) subcategory
		VARCHAR(255) control
		VARCHAR(255) product
		VARCHAR(255) country
		FLOAT qty_product
		FLOAT vl_product
		INTEGER year
		UUID category_uid
		TIMESTAMP created_at
		TIMESTAMP updated_at
	}
```