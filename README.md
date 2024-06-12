# Sistema de Biblioteca

Este é um projeto de sistema de biblioteca desenvolvido em Python com Flask, utilizando Bootstrap, CSS e HTML para a interface do usuário e MySQL como banco de dados.

## Instalação

Para executar este projeto, é necessário instalar algumas bibliotecas Python. Você pode instalá-las usando o seguinte comando:

```bash
pip install flask flask_sqlalchemy flask_migrate flask_wtf
```

Certifique-se também de ter o MySQL instalado na sua máquina.

## Configuração do Banco de Dados

Para configurar o banco de dados MySQL, você precisa criar um banco de dados com as seguintes tabelas:

```sql
CREATE TABLE `livro` (
  `id` int NOT NULL AUTO_INCREMENT,
  `titulo` text NOT NULL,
  `autor_id` int NOT NULL,
  `ano_publicacao` int DEFAULT NULL,
  `genero_id` int DEFAULT NULL,
  `disponivel` int DEFAULT '1',
  `url_da_capa` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `autor_id` (`autor_id`),
  KEY `genero_id` (`genero_id`),
  CONSTRAINT `livro_ibfk_1` FOREIGN KEY (`autor_id`) REFERENCES `autor` (`id`) ON DELETE CASCADE,
  CONSTRAINT `livro_ibfk_2` FOREIGN KEY (`genero_id`) REFERENCES `genero` (`id`) ON DELETE SET NULL
);

CREATE TABLE `autor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` text NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `emprestimo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `livro_id` int NOT NULL,
  `membro_id` int NOT NULL,
  `data_emprestimo` date NOT NULL,
  `data_devolucao` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `membro_id` (`membro_id`),
  KEY `fk_livro_id` (`livro_id`)
);

CREATE TABLE `genero` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `membro` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` text NOT NULL,
  `email` text,
  `telefone` text,
  PRIMARY KEY (`id`)
);
```

## Como Executar

Após instalar as dependências e configurar o banco de dados, você pode executar o projeto utilizando o seguinte comando:

```bash
python app.py
```

O sistema estará disponível em `http://localhost:5000`.

## Funcionalidades

O sistema oferece as seguintes funcionalidades:

1. **Autenticação de Usuários:** Cadastro de novos usuários, login de usuários existentes e controle de permissões de acesso.
2. **Gerenciamento de Livros:** Cadastro, atualização, remoção e busca de livros por diferentes critérios.
3. **Empréstimos:** Registro de empréstimos de livros para usuários, verificação de disponibilidade, definição de prazos de devolução e notificação de usuários.
4. **Devoluções:** Registro de devoluções de livros, cálculo de multas por atraso e atualização do status do livro.
5. **Reservas:** Permitir que os usuários reservem livros e notificação quando os livros reservados estão disponíveis.
6. **Gerenciamento de Usuários:** Atualização de informações de perfil, histórico de empréstimos e devoluções e cancelamento de conta de usuário.
7. **Administração do Sistema:** Monitoramento do banco de dados, configuração do sistema e geração de relatórios.
8. **Segurança:** Implementação de medidas de segurança para proteger informações sensíveis e prevenção contra ataques.
9. **Interface do Usuário:** Desenvolvimento de uma interface amigável e responsiva para facilitar a navegação e utilização do sistema.
10. **Integração com Banco de Dados:** Conexão com o banco de dados MySQL para armazenamento e recuperação de dados do sistema.

---

