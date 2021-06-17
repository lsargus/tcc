# Projeto de conclusão de curos
## IMPLEMENTAÇÃO DE TRANSFORMADORES DE POTÊNCIA E FLEXIBILIZAÇÃO DO APLICATIVO DE APLICAÇÃO DE FALTA EM LINHAS DE TRANSMISSÃO

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=lsargus_tcc&metric=alert_status)](https://sonarcloud.io/dashboard?id=lsargus_tcc)

Projeto de conclusão de curso desenvolvido pelo aluno Lucas Cauê Argus, sobre a orientação do professor Dr. Fabiano Gustavo Silveira Magrin.

## Para utilizar o programa é necessário a instalação dos seguintes programas:

- [Eclipse 3.7]

## Construção

para construir o projeto com python rode o seguinte comando 

```shell
$ pip install -r requirements.txt
```

O comando acima irá realizar o download de todas as dependencias do projeto

## Testes

Para rodar todos os testes, utilize o comando abaixo:

```
python -m unittest
```

Caso seja preciso rodar um unico teste em particular é possivel especificar o arquivo o arquivo em que o teste se encontra. Exemplo:

```
python -m unittest test/tcc/util/test_matriz.py
```

## Comando úteis

Caso novas dependencias tenham sido adicionadas é possivel atualizar o arquivo requirements.txt com o comando:

```shell
$ pip freeze > requirements.txt
```