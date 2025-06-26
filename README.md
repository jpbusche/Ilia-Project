# Fake Store de Pokemon

Este projeto foi desenvolvido com intuito de demonstrar meus conhecimentos para uma vaga de emprego na empresa Ilia.

## Como executar

Para executar esse projeto, basta seguir os passos abaixo:
* Clonar repositório do Git
* Baixar e montar as imagens
```
docker-compose build
```
* Executar as imagens
```
docker-compose up -d
```

Apos executados esses passos tanto o backend, tanto o front podem ser encontrados nesses links:
* [API](http://localhost:8000/docs)
* [Pagina Web](http://localhost:3000)


## Testes API

Para executar os testes do backend, basta seguir os passos abaixo:
* Clonar repositório do Git
* Criar um ambiente virtual (Python 3.12)
```
mkvirtualenv -p python3.12 fake_store
workon fake_store
```
* Instalar os requeriments
```
cd backend
pip install -r requeriments.txt
```
* Executar os testes com Nose
```
nose2 tests
```
