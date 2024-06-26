# Projeto Final de Curso

## Trabalho realizado por:
```
Rodrigo Amaro (22004525)
Daniel Granja (22002469)
```

## Docente
```
Manuel Pita (p5265)
```


## 0. Video:
https://youtu.be/KBxVKNbWeVo

## Passos para correr utilizando o docker:
### Pré-requesitos:
  #### Windows: 
    Ter o docker desktop instalado 
    Ter o git instalado
  #### Linux:
    Ter o docker instalado e a correr (para correr o daemon - sudo systemctl start docker | para verificar - sudo systemctl status docker)
    Ter o docker-compose instalado
    Ter o git instalado

### Fazer download e correr:
  #### Download windows & linux:
     Através do git cli - gh repo clone rodrigoamaro22004525/projetoTFC
     Através do nosso repositório - 
  <img src="https://github.com/rodrigoamaro22004525/projetoTFC/assets/79323898/41ee4d3b-557a-477a-a8c8-746518a88569">

  #### Correr no windows & linux:
      Abrir no diretório do projeto o cmd
  <img src="https://github.com/rodrigoamaro22004525/projetoTFC/assets/79323898/d00175ff-3089-43fb-a79f-cd046ba946bd">

      Fazer docker-compose build --up (build para compilar e up para começar as 2 imagens)
  <img src="https://github.com/rodrigoamaro22004525/projetoTFC/assets/79323898/6ee65e72-8055-4939-bea8-236b153c5c94">

  #### No fim é só entrar num browser
      Em Linux pode pôr o link 0.0.0.0:8000 (como na imagem)
      Em Windows normalmente não funciona o 0.0.0.0:8000, logo poderá usar o localhost:8000 ou 127.0.0.1:8000
  <img src="https://github.com/rodrigoamaro22004525/projetoTFC/assets/79323898/10ed26d5-70f5-4b29-b3ce-b8595bc01210">


## Imagem e texto para entrega final:
![entrega final](https://github.com/rodrigoamaro22004525/DEISI90-ALQI-DR-tutor-inteligente-para-estudar-interacoes-mediadas-por-algoritmos/assets/79323898/6b15d1fe-095e-4d7b-87b9-18974c40346f)

Este relatório detalha o desenvolvimento e implementação de um sistema inovador de busca de notícias utilizando modelos de LLM(large language models). Utilizamos tecnologias avançadas como Django para desenvolvimento web, Docker para consistência de ambiente e Nginx para gestão segura de tráfego web. Implementamos programas personalizados de datascrapping para arranjar notícias de várias fontes automaticamente, garantindo sempre conteúdo atualizado. Analisamos e visualizamos os dados coletados, proporcionando insights valiosos sobre a distribuição de notícias, temas abordados, e valência de sentimentos. Além disso, reforçamos a segurança com certificação SSL/TLS e facilitamos a acessibilidade através de subdomínios DuckDNS. A arquitetura escalável do AIDiAL KB foi projetada para suportar volumes crescentes de dados e demandas de usuários.

