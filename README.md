
# Docker AAD

## Sobre o projeto

Este projeto foi desenvolvido para a disciplina de Sistemas Operacionais.

O objetivo é executar uma aplicação Linux utilizando Docker, aplicando configurações de segurança, limites de recursos, registros de logs e reinício automático em caso de falha.

A aplicação foi desenvolvida em Python, utilizando Flask, e apresenta uma página web simples e uma rota para verificar o funcionamento do serviço.

## Integrantes

- Atos Gabriel
- Amy Galvão
- Dymylle Charis

## Tecnologias utilizadas

- Python 3.12
- Flask 3.1.1
- Docker
- Linux (imagem python:3.12-slim)
- Git e GitHub

## Arquivos do projeto

- `app.py`: código da aplicação Flask.
- `Dockerfile`: instruções para criar a imagem Docker.
- `requirements.txt`: dependências Python.
- `README.md`: apresentação e instruções do projeto.
- `RUNBOOK.md`: guia de operação e testes.

## Requisitos para executar

É necessário ter o Docker instalado e funcionando.

No Windows, pode ser utilizado o Docker Desktop com WSL 2.

## Como executar o projeto

### 1. Baixar o projeto

```bash
git clone https://github.com/AtrozGabriel/Docker-AAD.git
cd Docker-AAD
```

### 2. Criar a imagem Docker

```bash
docker build -t docker-aad .
```

### 3. Criar e iniciar o container

```bash
docker run -d --name docker-aad-container -p 8080:8080 --restart on-failure --memory 256m --cpus 0.5 -e LOG_LEVEL=INFO docker-aad
```

Esse comando configura:

- Execução em segundo plano.
- Acesso pela porta 8080.
- Reinício automático em caso de falha.
- Limite de 256 MB de memória.
- Limite de 0,5 CPU.
- Nível de log INFO.

### 4. Acessar a aplicação

Página inicial:

http://localhost:8080

Verificação de status:

http://localhost:8080/status

O serviço deve retornar um JSON informando que está online.

## Segurança

O container não executa a aplicação como usuário root.

No Dockerfile, foi criado o usuário `appuser`, com UID 10001.

Para verificar:

```bash
docker exec docker-aad-container id
```

## Configuração externa

A aplicação permite configurar variáveis de ambiente sem alterar o código.

- `PORTA`: porta utilizada pela aplicação. Padrão: 8080.
- `LOG_LEVEL`: nível dos logs. Padrão: INFO.

Exemplo:

```bash
docker run -d --name docker-aad-container -p 8080:8080 -e LOG_LEVEL=WARNING docker-aad
```

Esse exemplo deve ser executado quando não existir outro container com o mesmo nome.

## Logs

Para visualizar os registros da aplicação:

```bash
docker logs docker-aad-container
```

Os logs mostram informações sobre inicialização, acessos e falhas.

## Reinício automático

O container utiliza a política `on-failure`.

Isso significa que o Docker tenta reiniciar o container quando o processo principal termina com erro.

Para verificar a política:

```bash
docker inspect docker-aad-container --format '{{.HostConfig.RestartPolicy.Name}}'
```

Para consultar o número de reinícios:

```bash
docker inspect docker-aad-container --format '{{.RestartCount}}'
```

## Teste de falha controlada

A aplicação possui uma rota de teste que encerra o processo principal com código de erro 1.

Essa rota deve ser utilizada somente em ambiente local de testes.

No PowerShell:

```powershell
curl.exe -X POST http://localhost:8080/falha-teste
```

Depois, verificar o reinício:

```bash
docker inspect docker-aad-container --format '{{.RestartCount}}'
```

E confirmar que o serviço voltou:

```powershell
curl.exe http://localhost:8080/status
```

Durante nossos testes, o contador passou de 0 para 1 e o serviço voltou a responder normalmente.

## Parar o container

```bash
docker stop docker-aad-container
```

Para iniciá-lo novamente:

```bash
docker start docker-aad-container
```

## Repositório

https://github.com/AtrozGabriel/Docker-AAD
