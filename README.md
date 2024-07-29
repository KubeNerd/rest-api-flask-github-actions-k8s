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


## Explorando o Helm Charts
```bash
   # Pesquisar por um chart especifico
   helm search repo mongodb
   # Baixar pastas do chart
   helm pull bitname/mongodb --version 12.1.31
   # Adicionar repositório do chart nos charts locais
   helm repo add bitnami https://charts.bitnami.com/bitnami
   # Descompactar o tar
   tar xfvz mongodb-12.1.31.tgz
   # Exibir manifestos completos com base nos templatesls
   helm template .
   # Sobscrever imagem
   helm template . --set image.tag=5.0.8
   # Instalando mongo apartir do diretório atual
   helm upgrade --install mongodb -n [namespace] .
   # Instalando da forma correta agora
   helm upgrade --install mongodb --set image.tag=5.0.8 --set auth.rootPassword="root" -n [namespace] .
   
   helm upgrade --install mongodb --set image.tag=5.0.8 --set auth.rootPassword="development@123456!" -n [namespace] .

```

## Explorando o Kubectl
```bash
   # Deploy da api no kubernetes
   kubectl create deployment --image [deployment-name] [image-name] --dry-run=client -o yaml >> kubernetes/manifests/deployment.yaml
```

## Secrets no Kubernetes
O ideal é criar secrets de forma declarativa. Mas também é interesante sabermos como criar via linha de comando caso necessário.

```bash
kubectl create secret generic --from-literal=SECRET_NAME=value
```

## Criando apartir de um arquivo .env
```bash
kubectl create secret generic [my-secrets-name] --from-env-file=.env-file-name -n [namespace-name]
```

**Referências:**: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_create/kubectl_create_secret_generic/

## Expondo app apartir do deployment e gerando o manifesto - Service

```bash
   kubectl expose deploy [app-name] --port [number] --target-port [number] --dry-run=client -o yaml >> service.yaml

   # Ou
      kubectl expose deploy [app-name] --port [number] --target-port [number] --dry-run -oyaml | kubectl neat >> service.yaml

```
**Refereências**: 
   - https://kubernetes.io/docs/concepts/services-networking/service/
   - https://kubernetes.io/docs/reference/kubectl/generated/kubectl_expose/

## Bonus:
Para otimizar o processo de deploy local, é possivel fazer o upload das imagens para dentro do cluster/kind.

Após fazer build de uma imagem docker, podemos carrega-la para dentro do cluster, assim.

```bash
   # Build da imagem
   docker build -t [image-name]:[tag-name] ./
   # Upando a imagem para dentro do cluster
   kind load docker-image [image-name]:[tag-name]

   #Por final, acesse o container do cluster, via lens, ou da forma que achar melhor, e liste as imagens com o crictl.
   crictl images
```


### crictl
O crictl é uma ferramenta de linha de comando usada para interagir com runtimes de contêineres que seguem a Container Runtime Interface (CRI) do Kubernetes. Ele permite inspecionar e gerenciar contêineres e pods no cluster. Aqui estão algumas instruções básicas para usar crictl

Para instalar o crictl, você pode seguir as instruções https://github.com/kubernetes-sigs/cri-tools


```bash
VERSION="v1.24.0"
wget https://github.com/kubernetes-sigs/cri-tools/releases/download/$VERSION/crictl-$VERSION-linux-amd64.tar.gz
tar zxvf crictl-$VERSION-linux-amd64.tar.gz -C /usr/local/bin
```

```bash
crictl --version

```

Você pode precisar configurar o crictl para se comunicar com o runtime de contêiner. Por exemplo, para configurar com o containerd, crie um arquivo de configuração


**Configuração**
Você pode precisar configurar o crictl para se comunicar com o runtime de contêiner. Por exemplo, para configurar com o containerd, crie um arquivo de configuração:

```bash
sudo nano /etc/crictl.yaml

```
Adicione o seguinte conteúdo:
```yaml
   runtime-endpoint: unix:///var/run/containerd/containerd.sock
```

# Comandos Básicos

Aqui estão alguns comandos úteis do `crictl`:

Listar contêineres:

```bash
crictl ps
```
Listar todos os contêineres, incluindo os que não estão em execução:

```bash
crictl ps -a
```
Para mais infos e exemplos: https://github.com/containerd/containerd/blob/main/docs/cri/crictl.md
Article: https://vineetcic.medium.com/mapping-from-dockercli-to-crictl-life-after-docker-is-cri-a39ea5649d6c



# Novas referências: 
   Scann de segurança https://github.com/PyCQA/bandit