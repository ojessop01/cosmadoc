# The Durham Azimuth Cloud Facility (DACF)

Azimuth is a cloud system hosted within COSMA.

Projects with accounts on Azimuth can manage their own nodes, Slurm clusters, Kubernetes clusters, etc.

## Kubernetes Access

The Azimuth Cloud Portal allows you to deploy Kubernetes clusters and manage them with `kubectl`, `helm` and `k9s`.

To access a Kubernetes cluster you need access to the [Azimuth portal](https://portal.azimuth.cosma.dur.ac.uk).
Download the Kubernetes configuration file (usually called `kubeconfig`) to your local machine, and install `kubectl` (plus `helm` and `k9s` if needed).

You can check your local installation with:

```bash
kubectl version --client
helm version
k9s version
```

To interact with a cluster, point your terminal to the downloaded config file:

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

`k9s` is a terminal user interface for Kubernetes. It can be useful for checking pods, logs, deployments, services, config maps, and secrets.

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
export KUBECONFIG=$HOME/.kube/config:$HOME/ml-intro.yaml:$HOME/test-cluster.yaml
```

## JupyterHub Configurations

Jupyter notebooks run as Kubernetes pods inside the `jupyterhub` namespace.  Different reproducible deployments can be created via Helm charts. To maintain and extend user resources, you can build different Docker images such as GPU-enabled, CPU-based, or C/C++ notebooks. For more details please check [here](https://z2jh.jupyter.org/en/stable/resources/reference.html).

When you want to debug which image is running on a notebook pod, you can use the commands below (replace `POD` with the specific pod name if more than one `jupyter-` pod is running):

Checking which image is running:

```bash
POD=$(kubectl -n jupyterhub get pods -o name | grep -m1 jupyter- | sed 's|pod/||')

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

If you are developing a new course, build kernels on your local machine to deploy on Azimuth. Create a directory with a `Dockerfile` alongside your requirements and course materials:

```bash
docker build -t quay.io/<username>/<image>:<tag> .
docker push quay.io/<username>/<image>:<tag>
```

_Note:_ If you are using macOS on ARM processors, use `docker buildx` (with `--platform linux/amd64`) to build cross-platform images.

After building and pushing the image to a container registry (e.g. Quay), reference the image in `apps/jupyterhub/values.yaml`.
You need access to that repository to commit your deployment:

```bash
git add .
git commit -m "Image added with <tag>"
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

## Limitations

The Azimuth cloud system is still under development, meaning that some issues or bugs in JupyterHub may be present. Please contact cosma-support@durham.ac.uk if you come across anything odd when deploying your course on Azimuth cloud.
