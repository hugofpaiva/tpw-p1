# App Store
http://hugofpaiva.pythonanywhere.com/
## Introdução
Este trabalho consistiu na criação de uma _Web App_ para _desktop_, cujo objetivo principal é a disponibilização de uma Loja de aplicações. Cada aplicação tem associado
um  ( ou mais) plano(s) de pagamento ( grátis, mensal e anual ), uma ou mais categorias, e também um developer aliado ( cada developer pode ter mais do que uma aplicação). É permitida a interação dos clientes com os produtos, através da efetuação das compras destes produtos ( aplicações), adicionar ou remover estes aos favoritos, ou realizar "reviews" das aplicações. 

## Dataset 
Aguns dos dados têm como base o seguinte _dataset_: 
https://www.kaggle.com/usernam3/shopify-app-store

As imagens do produtos, desenvolvedores, categorias, entre outros dados foram utilizados.

## Autenticação na plataforma

Para utilizar o nosso sistema, fornecemos duas contas base:
    - Cliente:
        ```
        username: cliente12    
        password: admin111
        ``` 
    - Administrador: 

        ```
        username: admin
        password: admin
        ```

## Lado do cliente

Depois de efetuar o login:

    Permite ver o username e o balance da conta no canto superior direito.

    Na página Shop:
        - Permite utilizar os filtros de forma dinâmica em todos os seus campos para encontrar as aplicações desejadas, bem como as ordenações.
        - Em cada preview da app, encontramos a foto, nome e rating médio (estrelas)
        
    Clicando numa app:
        - Permite ver os detalhes da app.
        - Permite adicionar/remover dos favoritos, comprar a app, ver e adicionar/editar reviews.
        
    Na página About us:
        - Apenas contém uma página informativa do coteúdo da aplicação.
    
    Clicando no nome no canto superior direito:

        Na aba General:
            - Permite alterar as definições gerais do cliente.
        Na aba Password:
            - Permite alterar a password.
        Na aba Favorites:
            - Permite ver uma lista dos favoritos do utilizador, bem como um botão que redireciona para o produto.
        Na aba My Apps:
            -Permite ver uma lista de apps compradas pelo utilizador


## Lado do Admin

Depois de efetuar o login:

    Permite ver todas as informações já referidas anteriormente no cliente.

    Na pá





