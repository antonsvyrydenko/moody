# Moody

Basic project to test `k8s` + `Kafka`

For this project `DigitalOcean` `k8s` cluster was used.

### Requirements

- `k8s` cluster configured
- `docker` installed locally
- `Python 3.10` installed locally
- `kubectl` installed locally
- `Kafka` server configured
- `DockerHub` account

### Installation

1. Configure `k8s`

   1.1 After `k8s` cluster creation just follow guide at `Getting Started with Kubernetes` section.

   1.2 Download configuration file. When downloaded it's name should be something like: `CLUSTER_NAME-kubeconfig.yaml`

   1.3 Install `kubectl` locally:
   
     ``curl -LO https://dl.k8s.io/release/`curl -LS https://dl.k8s.io/release/stable.txt`/bin/linux/amd64/kubectl``
   
     `chmod +x ./kubectl`

     `sudo mv ./kubectl /usr/local/bin/kubectl`

     `kubectl version --client`

   1.4 Check availability of cluster by executing different calls:
   
     `kubectl --kubeconfig=/<pathtodirectory>/CLUSTER_NAME-kubeconfig.yaml get nodes`

     `kubectl --kubeconfig=/<pathtodirectory>/CLUSTER_NAME-kubeconfig.yaml cluster-info`

   1.5 Set `Kafka` secrets:

     `kubectl --kubeconfig=/<pathtodirectory>/CLUSTER_NAME-kubeconfig.yaml create secret generic kafka-path --from-literal=KAFKA_TOPIC=KAFKA_TOPIC --from-literal=KAFKA_SERVER=SERVER_URL:9092`

   1.6 Get secrets info:

     `kubectl --kubeconfig=/<pathtodirectory>/CLUSTER_NAME-kubeconfig.yaml get secrets`

     `kubectl --kubeconfig=/<pathtodirectory>/CLUSTER_NAME-kubeconfig.yaml describe secret kafka-path`

   1.7 Login to `docker` locally, enter your username and password when prompted

     `docker login`

   1.8 Create `k8s` secret for `docker` auth:

     `kubectl --kubeconfig=/<pathtodirectory>/CLUSTER_NAME-kubeconfig.yaml create secret generic dockerhubkey --from-file=.dockerconfigjson=/home/USER/.docker/config.json --type=kubernetes.io/dockerconfigjson`

   1.9 Describe secrets

     `kubectl --kubeconfig=/<pathtodirectory>/CLUSTER_NAME-kubeconfig.yaml get secret -o yaml`

2. Build and deploy app

   2.1 `docker build -t moody:latest .`

   2.2 `docker tag moody:latest PRIVATE_REPO/moody:latest`

   2.3 `docker push PRIVATE_REPO/moody:latest`

   2.4 Update `deployment.yaml` - set repo and image new hash (get it on `DockerHub` dashboard)

     `image: PRIVATE-REPO/IMAGE@sha256:UNIQUE_HASH`

   2.5 Deploy app

     `kubectl --kubeconfig=/<pathtodirectory>/CLUSTER_NAME-kubeconfig.yaml apply -f deployment.yaml`

   2.6 Check nodes and pods

     `kubectl --kubeconfig=/<pathtodirectory>/CLUSTER_NAME-kubeconfig.yaml get nodes`

     `kubectl --kubeconfig=/<pathtodirectory>/CLUSTER_NAME-kubeconfig.yaml get pods`

     `kubectl --kubeconfig=/<pathtodirectory>/CLUSTER_NAME-kubeconfig.yaml describe pods`

   2.7 Check environment of pod

     `kubectl --kubeconfig=/<pathtodirectory>/CLUSTER_NAME-kubeconfig.yaml exec -it POD_ID -- env`

   2.8 Check logs of pod

     `kubectl --kubeconfig=/<pathtodirectory>/CLUSTER_NAME-kubeconfig.yaml logs POD_ID`

3. Create `Kafka` topic for app

    3.1 Login to server with `Kafka` and get into the folder with `Kafka` scripts

       `ssh root@YOUR_KAFKA_SERVER` 

       `cd ~/kafka_src/kafka_VERSION/bin`

    3.2 Create topic
  
       `./kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 2 --topic KAFKA_TOPIC`

    3.3 Watch topic log

       `./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic KAFKA_TOPIC --from-beginning`

### Usage

1. Install and configure environment

  `virtualenv -p python3.10 venv`

  `. venv/bin/activate`

  `pip install -r requirements.txt`

2. Set `Kafka` value in `secrets.file`

3. Start response listener

  `./run.sh listener`

4. Send request for mood handler in another terminal tab

  `. venv/bin/activate`

  `./run.sh request curious` 

5. Check `moody` app response in terminal tab where `listener` were launched
