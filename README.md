#  Omnirobot

Omnirobot é um bot escrito na linguagem de programação Python para o Pokémon Showdown, tendo como foco a otimização  da jogatina de minigames da sala Português da plataforma.


# Instalação e execução do bot

Para executar o script do bot em sua máquina (ou em um servidor remoto), você irá precisar das seguintes ferramentas instaladas:

PostgreSQL 16
PgAdmin 4 (Normalmente instalado juntamente com o PostgreSQL)
Python 3.10 ou superior
git 2.35.1 ou superior

Siga os seguintes passos:

- Clone o repositório via git utilizando o comando `git clone https://github.com/GabrielDSS0/Omnirobot.git`
- Abra um prompt de comando dentro do diretório do repositório que acabou de clonar, e digite `pip install -r requirements.txt`. Este comando instalará todos os pacotes necessários para a execução do código Python.
- Abra o pgAdmin4 e crie um banco de dados novo, assim como um schema novo. Guarde os nomes do banco de dados e do schema.
- Crie, dentro da pasta do bot, arquivos chamados `config.json` e `db.json`. 
- Copie o que está no arquivo `config-example.json` e coloque dentro do `config.json`.
-  Copie o que está no arquivo `db-example.json` e coloque dentro do arquivo `db.json.`
- Dentro do arquivo `config.json`, coloque as informações principais do bot, como username, senha, avatar, etc. Caso queira trocar o prefixo dele, este é o arquivo certo.
- Dentro do arquivo `db.json`, coloque no campo `database` o nome do banco de dados que criara, no campo `password` a senha que você definiu para acesso do servidor do PostgreSQL, e no campo `schema` o schema definido.
- Execute o arquivo `run.py`.


## Outros detalhes

- O arquivo `pokemon-showdown-uris.txt` contém todas as uris para acessar o servidor do Pokémon Showdown. Caso queira se conectar a um servidor local iniciado em sua máquina, utilize a primeira uri. As duas últimas uris acessam o servidor global do Pokémon Showdown.
- O arquivo `saveobjects.pkl`, criado após iniciar o bot pela primeira vez, é responsável pelo backup de informações dos jogos que ocorrem em salas de groupchat, para que não se percam caso o bot seja desligado repentinamente. O nome deste arquivo pode mudar conforme configuração em `config.json`.
- O arquivo `commands.html` contém as informações resumidas dos comandos que serão mandadas em uma caixa HTML caso algum usuário no Pokémon Showdown utilize o comando `@commands`.
