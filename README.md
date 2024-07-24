# Proposta do Projeto

Este projeto evoluiu para rodar no Kubernetes, integrando diversas ferramentas de DevOps para melhorar a automação, qualidade e segurança do código, além de facilitar o deployment tanto em ambientes locais quanto na nuvem (AWS EKS).

## Ferramentas Utilizadas
- Flask
- Docker
- Kubernetes (Kind, Minikube, K3s)
- Helm
- Terraform
- Vagrant
- Ansible
- GitHub Actions


## Neste segundo módulo eu proponho o seguinte:

1. **Melhorar a API adicionando mais 2 rotas (endpoints):**
   - `/user/<cpf> (DELETE)` para deletar um usuário do banco de dados.
   - `/user (PATCH)` para atualizar um usuário existente.

2. **Criar um endpoint para health check que teste efetivamente a conexão com o banco de dados.** O objetivo é que o nosso pod não receba tráfego enquanto o banco não estiver respondendo.

3. **Adicionar novas estratégias para garantir a qualidade de código e também da perspectiva de segurança.**

4. **Construir um cluster local (na sua própria máquina) utilizando ferramentas como Kind, Minikube, K3s.**

5. **Criar manifestos Kubernetes para fazer o deploy da aplicação.**

6. **Adaptar o Makefile para deployar no cluster de desenvolvimento criado no passo 2.**

7. **Evoluir os manifestos de forma empacotada usando um Helm Chart.**

8. **Construir um cluster EKS na AWS utilizando Terraform.**

9. **Adaptar o Makefile para deployar no EKS.**

10. **Criar uma estratégia de deployment com o mínimo possível de erros.**

11. **Evoluir a pipeline no GitHub Actions adicionando os novos testes e deployando no EKS.**


Novas referências: 
   Scann de segurança https://github.com/PyCQA/bandit