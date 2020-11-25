
# [App Store](http://hugofpaiva.pythonanywhere.com/)

Este trabalho consistiu na criação de uma _Web App_ com enfoque no _desktop_, cujo objetivo principal é a disponibilização de uma loja de aplicações em _Django_.

Cada aplicação tem associado um ou mais plano(s) de pagamento (grátis, mensal e anual), uma ou mais categorias e também um developer. É permitida a interação dos clientes com as aplicações, através de compras, adição ou remoção destes como favoritos, ou escrever _reviews_.

### Funcionalidades de um cliente

**Após efetuação do *login*:**

- É possível ver o *username* e o saldo da conta no canto superior direito.
- Caso o cliente exista alguma aplicação que expire a subscrição do plano de pagamento na próxima semana, é disponibilizada a opção de pagar ou não. _Para facilitar o teste do Professor a esta funcionalidade, foi colocada uma aplicação com a data de expiração a **30 de novembro** sendo que até lá, o aviso deverá aparecer._

**Na página Shop:**

- É permitida a utilização dos filtros de forma dinâmica em todos os seus campos para encontrar as aplicações desejadas, bem como as ordenações.

- Em cada *preview* de aplicação, encontra-se a foto, nome e *rating* médio (estrelas)

**Clicando numa aplicação:**

- É possível ver os detalhes da *app*.

- É permitido adicionar/remover dos favoritos, comprar a *app*, ver e adicionar/editar *reviews*.

  

**Clicando no nome no canto superior direito (nome do utilizador):**
  
Na aba General:

- É permitida a alteração das definições gerais do cliente

Na aba Password:

- É permitida a alteração da password.

Na aba Favorites:

- É permitdo ver a lista dos favoritos do utilizador, bem como um botão que redireciona para o produto.

Na aba My Apps:

-É permitido ver uma lista de *apps* compradas pelo utilizador com informação relevantes como a data de expiração de uma compra, caso seja do tipo de um plano de subscrição.


## Funcionalidades de um administrador
  
 **Depois de efetuar o login:**

- É permitida a visualização de todas as informações já referidas anteriormente no cliente.

**Clicando no nome:**

- É permitido fazer as mesmas alterações e/ou visualizações que o cliente

**Além disso, clicando na aba Admin:**

Na aba Purchases:

- É permitido ver a lista de todas as compras feitas na aplicação _web_, bem como qual o cliente que efetuou cada compra.

Na aba Users:

- É permitido ver a lista de todos os utilizadores da aplicação.

- É permitido adicionar saldo às contas dos clientes.

Na aba Applications:

- É permitido ver a lista de todas os produtos disponíveis na aplicação _web_.

- É permitido editar os campos dos produtos.

- No botão _Add Product_, é permitido adicionar produtos novos e um plano de pagamento base associado a este produto.

Nas abas _Add developer/Add category_:

- É permitida a adição de novos _developers/categories_

  
  

## Alguns detalhes de implementação:

Para as funções de criação de dados e edição foram utilizados _forms_ do _Django_.

A implementação base de filtros na página _shop_ utilizou _Django Filters_ bem como a paginação do _Django_.

Todas as _packages_ necessárias estão no ficheiro `requirements.txt`.
  

## Autenticação na plataforma

Para utilizar o sistema, são fornecidas duas contas base:

**Cliente:**
```
username: cliente12
password: admin111
```
**Administrador:**
```
username: admin
password: admin
```

## Dataset

Alguns dos dados têm como base o seguinte _dataset_:

https://www.kaggle.com/usernam3/shopify-app-store

As imagens do produtos, desenvolvedores, categorias, entre outros dados foram utilizados.



