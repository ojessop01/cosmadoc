# The Durham Azimuth Cloud Facility (DACF)

Azimuth is a cloud system hosted within COSMA.

Projects with accounts on Azimuth can manage their own nodes, Slurm clusters, Kubernetes clusters, etc.

# Kubernetes Access

The Azimuth Cloud Portal allow us to deploy Kubernetes clusters using `kubectl` and `k9s`.

To access a Kubernetes cluster you need access to the [Azimuth portal](https://portal.azimuth.cosma.dur.ac.uk).
If you want to have more details about Kubernetes cluster, a Kubernetes configuration file, usually called `kubeconfig`
should be download to your local machine. To be able to use this cluster `kubectl` installed on your local machine. Optional but also recommended: `k9s`

You can check if all installation is good so far by:

```bash
kubectl version --client
helm version
k9s version
```

To interact with a cluster, you sould point your terminal to the downloaded config file.

```bash
export KUBECONFIG=~/.kube/ml-intro.yaml
```

You can check that access works:

```bash
kubectl cluster-info
kubectl get nodes
```

Example output:

```text
NAME                                  STATUS   ROLES           VERSION   INTERNAL-IP
ml-intro-control-plane-65mpf          Ready    control-plane   v1.34.6   x.x.x.x
ml-intro-control-plane-l4rv2          Ready    control-plane   v1.34.6   x.x.x.x
ml-intro-control-plane-ntm9r          Ready    control-plane   v1.34.6   x.x.x.x
ml-intro-ml-intro-69ngd-ckrhh         Ready    worker          v1.34.6   x.x.x.x
```

---

## Using K9s

`k9s` is a terminal user interface for Kubernetes. It is can be useful for checking pods, logs, deployments, services, config maps, and secrets.

```bash
k9s
```
## Checking the Current Context

Kubernetes commands are run against the current context in your kubeconfig.

```bash
kubectl config current-context
```

List all available contexts:

```bash
kubectl config get-contexts
```

Switch context:

```bash
kubectl config use-context <context-name>
```

Example:

```bash
kubectl config use-context ml-intro-admin@ml-intro
```

## Multiple Kubernetes Clusters

Users may have access to more than one Kubernetes cluster, for example a GPU cluster,ML cluster etc. Kubernetes uses a file called a `kubeconfig` to store cluster connection details, users, namespaces, and contexts.

Kubernetes can merge multiple kubeconfig files using the KUBECONFIG environment variable:

```bash
export KUBECONFIG=$HOME/.kube/config:$HOME/ml-intro.yaml:$HOME//test-cluster.yaml
```

## JupyterHub Configurations

Jupyter notebooks runs as a Kubernetes pod inside the JupyterHub namespaces.  In those namespaces, diffrent reproducible deployments can be created via Helm charts. To maintaine and extend user resoruces, it could build unlike Docker images such as, GPU-enabled notebook, CPU-based notebook, C/C++ notebook etc. For more details please check [here](https://z2jh.jupyter.org/en/stable/resources/reference.html)

When you want to debug which image is running on which notebook helm chart, you could use below useful commands.

Checking which image is running: 

```bash 
POD=$(kubectl -n jupyterhub get pods -o name | grep jupyter- | sed 's|pod/||')

kubectl -n jupyterhub get pod "$POD" \
  -o jsonpath='{.spec.containers[?(@.name=="notebook")].image}{"\n"}'
```

Verifying image digest:

```bash
kubectl -n jupyterhub get pod "$POD" \
  -o jsonpath='{.status.containerStatuses[?(@.name=="notebook")].imageID}'
```

To check where single-user pod mounted:

```bash
kubectl -n jupyterhub get pod "$POD" \
  -o jsonpath='{range .spec.containers[?(@.name=="notebook")].volumeMounts[*]}{.name}{" -> "}{.mountPath}{"\n"}{end}'
```

**Please note that if the storage mounted as a Persistent Volume Claim you have to move your Jupyter server config to somewhere else from the directory you put in. Because the configs will be hidden by mounted volume. So, it would not work what you apply into the helm chart values**

__NOTE__: Jupyterhub configurations should generally be provided as explicit assignments rather than by setting existing configuration values (e.g. `getattr(..., "tornado_settings")`). Please avoid relying on existing runtime values inside `jupyter_server_config.py`; instead assign complete configuration objects directly (e.g. `c.ServerApp.tornado_settings = {...}`).


### Creating Profiles for Courses

If you are developing a new course, you have to build kernels on your local machine to deploy on Azimuth. To do that you have to create a directory having Dockerfile to pass your kernels along side requirtments and course materials. 

```bash
docker build -t quay.io/<username>/<image>:<tag> .
docker push quay.io/<username>/<image>:<tag>
```

_Note:_ If you are using MacOs ARM procceses you have to use `buildx` to create cross platform working images. 

After building and pushing the image to a container registry (e.g. Quay), then reference the image should be in `apps/jupyterhub/values.yaml`. 
You have to access that repo to be able to commit your deployment.

```bash
git add .
git commit - m "Image added with <tag>"
git push origin
```

Once the configuration is committed and you need to deploy via FluxCD:

```bash
flux get helmreleases -A
flux reconcile source git flux-system -n flux-system
flux reconcile kustomization apps -n jupyterhub --with-source
flux reconcile helmrelease jupyterhub -n jupyterhub --force
```

The new profile becomes available to users when they launch JupyterHub from Moodle.

# Limitations

The system of Azimuth cloud still under the development phase - meaning that some issues/bugs in JupyterHub may be present. Please do let us know if you come across anything odd deploying your course on Azimuth cloud.
