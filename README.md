# MVP_Sprint3_B

Este pequeno projeto faz parte do MVP do módulo da disciplina **Desenvolvimento Back-end Avançado** 

As principais tecnologias que serão utilizadas aqui é o:
 - [Flask](https://flask.palletsprojects.com/en/2.3.x/)
 - [Flask-RESTX](https://flask-restx.readthedocs.io/en/latest/)

---
### Interoperabilidade

Esta aplicação interage com outra API também escopo deste MVP. Para visualizar a outra API acesse:
 - [MPV_Sprint3_A](https://github.com/Thi4gobit/MVP_Sprint3_A)

---
### Instalação

Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

---
### Executando a aplicação

Para executar a API basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

---
### Acesso no browser

Abra o [http://localhost:8000/#/](http://localhost:8000/#/) no navegador para verificar o status da API em execução.

---
### Como executar através do Docker

Certifique-se de ter o [Docker](https://docs.docker.com/engine/install/) instalado e em execução em sua máquina.

Cosiderando a interoperabilidade com o **MPV_Sprint3_B** crie uma rede para inerligar as duas aplicações.

Para criar uma rede no docker execute **como administrador** o seguinte comando:

```
$ docker network create mvp
```

Para verificar se a rede foi criada execute:

```
$ docker network ls
```

Confira se a rede foi criada.

Navegue até o diretório que contém o Dockerfile e o requirements.txt no terminal.
Execute **como administrador** o seguinte comando para construir a imagem Docker:

```
$ docker build -t django .
```

Uma vez criada a imagem, para executar o container basta executar, **como administrador**, seguinte o comando:

```
$ docker run -d --name flask --network mvp -p 5000:5000 django
```

Uma vez executado, para acessar a API, basta abrir o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador.


### Dicas

>Para mais comandos, veja a [documentação do docker](https://docs.docker.com/engine/reference/run/).
