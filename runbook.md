
# RUNBOOK — Docker AAD

## 1. Objetivo

Este documento apresenta os procedimentos para executar, verificar e testar a aplicação Docker AAD.

Os testes foram realizados localmente no Windows, utilizando Docker Desktop, VS Code e PowerShell.

## 2. Preparação

Antes de começar:

1. Abrir o Docker Desktop.
2. Aguardar o Docker iniciar.
3. Abrir a pasta do projeto no VS Code.
4. Abrir o terminal PowerShell.

Verificar se o Docker está funcionando:

```powershell
docker version
```

## 3. Construir a imagem

Na pasta do projeto, executar:

```powershell
docker build -t docker-aad .
```

## 4. Criar e iniciar o container

```powershell
docker run -d --name docker-aad-container -p 8080:8080 --restart on-failure --memory 256m --cpus 0.5 -e LOG_LEVEL=INFO docker-aad
```

Se o container já existir e estiver parado, utilizar:

```powershell
docker start docker-aad-container
```

Verificar o funcionamento:

```powershell
docker ps
```

O container deve aparecer com o status `Up`.

## 5. Testar a aplicação

Acessar pelo navegador:

http://localhost:8080

Verificar o status pelo PowerShell:

```powershell
curl.exe http://localhost:8080/status
```

Resultado esperado:

```json
{
  "porta": 8080,
  "servico": "Docker AAD",
  "status": "online"
}
```

## 6. Verificar o usuário do container

```powershell
docker exec docker-aad-container id
```

Resultado esperado: UID 10001, demonstrando que a aplicação não executa como root.

## 7. Verificar os limites de recursos

```powershell
docker inspect docker-aad-container --format 'Memoria={{.HostConfig.Memory}} bytes | CPUs={{.HostConfig.NanoCpus}}'
```

Resultados esperados:

- Memória: 268435456 bytes (256 MiB).
- CPU: 500000000 NanoCPUs (0,5 CPU).

## 8. Verificar a política de reinício

```powershell
docker inspect docker-aad-container --format '{{.HostConfig.RestartPolicy.Name}}'
```

Resultado esperado:

```text
on-failure
```

## 9. Consultar os logs

```powershell
docker logs --tail 30 docker-aad-container
```

Os logs devem mostrar a inicialização, as requisições e os erros registrados pela aplicação.

## 10. Testar o reinício automático

ATENÇÃO: realizar este teste somente no ambiente local.

Primeiro, consultar o número atual de reinícios:

```powershell
docker inspect docker-aad-container --format 'Reinicios={{.RestartCount}} | Estado={{.State.Status}}'
```

Aguardar pelo menos 10 segundos com o serviço funcionando.

Provocar uma falha controlada:

```powershell
curl.exe -X POST http://localhost:8080/falha-teste
```

A requisição pode apresentar a mensagem `Empty reply from server`, porque o processo é encerrado durante a resposta.

Aguardar alguns segundos e consultar novamente:

```powershell
docker inspect docker-aad-container --format 'Reinicios={{.RestartCount}} | Estado={{.State.Status}}'
```

Resultado esperado:

- O número de reinícios aumenta.
- O estado retorna para `running`.

Confirmar que a aplicação voltou a funcionar:

```powershell
curl.exe http://localhost:8080/status
```

Consultar os logs:

```powershell
docker logs --tail 30 docker-aad-container
```

Os logs devem mostrar a falha controlada e a nova inicialização.

## 11. Testar configuração externa

Para verificar as variáveis de ambiente:

```powershell
docker inspect docker-aad-container --format '{{range .Config.Env}}{{println .}}{{end}}'
```

Procurar a variável:

```text
LOG_LEVEL=INFO
```

O nível pode ser alterado ao criar um novo container utilizando `-e LOG_LEVEL=WARNING`.

## 12. Encerrar normalmente

```powershell
docker stop docker-aad-container
```

Confirmar que o container parou:

```powershell
docker ps -a
```

## 13. Evidências para o relatório

Guardar capturas de tela demonstrando:

1. Imagem Docker construída.
2. Container em execução.
3. Aplicação funcionando no navegador.
4. UID diferente de zero.
5. Limites de memória e CPU.
6. Política de reinício `on-failure`.
7. Contador de reinícios aumentando após a falha.
8. Aplicação respondendo após o reinício.
9. Logs mostrando a falha e a recuperação.
10. Variáveis de ambiente configuradas.

## 14. Problemas comuns

### Docker não está funcionando

Abrir o Docker Desktop e aguardar sua inicialização.

### Nome do container já está em uso

Verificar os containers existentes:

```powershell
docker ps -a
```

Se o container estiver parado, utilizar `docker start`.

### Porta 8080 ocupada

Verificar se já existe outro serviço utilizando essa porta.

### Alterações no app.py não aparecem

Reconstruir a imagem e recriar o container para aplicar as alterações.
