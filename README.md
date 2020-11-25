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

Clicando no nome no canto superior direito(nome do utilizador):

    Na aba General:
        - Permite alterar as definições gerais do cliente.
    Na aba Password:
        - Permite alterar a password.
    Na aba Favorites:
        - Permite ver uma lista dos favoritos do utilizador, bem como um botão que redireciona para o produto.
    Na aba My Apps:
        -Permite ver uma lista de apps compradas pelo utilizador


## Lado do Admin

### Depois de efetuar o login:


Permite ver todas as informações já referidas anteriormente no cliente.

Clicando no nome:

- Permite fazer as mesmas alterações e/ou visualizações que o cliente

Alem disso, clicando na aba Admin:
    
Na aba Purchases:

- Permite ver uma lista de todas as compras feitas na aplicação, bem como qual o cliente que efetuou cada compra.

na aba Users:

- Permite ver uma lista de todos os utilizadores da aplicação.
- Permite adicionar dinheiro às contas dos clientes. 

na aba Applications:

- Permite ver uma lista de todas os produtos disponíveis na Aplicação.
- Permite editar os campos dos produtos.
- No botão Add Product permite adicionar produtos novos, e um plano de pagamento base associado a este produto.

nas abas Add developer/Add category:

- Permite adicionar novos developers/categories


## Pontos fundamentais da nossa aplicação:

Para criar conta foi utilizado o UserCreationForm do django.
Para alterar as definições base da conta foi utilizado o UserChangeForm do django.
Para alterar a passowrd da conta foi utilizado o PassowrdChangeForm do django.

Foi utilizado django filters para os filtros.

Foi utilizado django pagination para a paginação. 

Todas as instalações necessárias estão no ficheiro `requirements.txt`.
`







#QUANDO A APLICAçÂO VAI EXPIRAR
#METER BD DO PYTHON ANYWHERE AQUI
#Verificar se o cliente 12 está top
    