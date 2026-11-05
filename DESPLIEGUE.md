# Despliegue: Docker Hub, EC2 y GitHub Pages

Las subidas las hace el autor. Esta guía asume la imagen
`andresperez3/bohr-h-andresdperezc:0.1.0` y Streamlit en el puerto **8501**,
**sin contraseña** (opción B del proyecto).

## 1. Docker Hub

Usuario: `andresperez3`.

```bash
docker login
docker build -t andresperez3/bohr-h-andresdperezc:0.1.0 .
docker push andresperez3/bohr-h-andresdperezc:0.1.0
```

En cualquier PC (Windows, Linux o macOS):

```bash
docker pull andresperez3/bohr-h-andresdperezc:0.1.0
docker run --rm -p 8501:8501 andresperez3/bohr-h-andresdperezc:0.1.0
```

Abra http://localhost:8501. No hace falta Tkinter.

Si cambia el código, reconstruya la imagen y, si ya empujó el tag `0.1.0`,
use un tag nuevo (`0.1.1`) o `--platform` no es necesario en este proyecto
(la imagen es `python:3.12-slim` linux/amd64; en Mac Apple Silicon:
`docker run --platform linux/amd64 ...` si Docker no emula solo).

## 2. AWS EC2 (Free Tier) — GUI abierta a internet, sin contraseña

Objetivo: `http://IP-PUBLICA:8501` abre la misma GUI.

### 2.1 Lanzar la instancia

1. Consola AWS → EC2 → *Launch instance*.
2. Nombre: `bohr-gui` (o el que quiera).
3. AMI: **Amazon Linux 2023** o **Ubuntu 24.04** (Free Tier).
4. Tipo: **t2.micro** o **t3.micro**.
5. Par de claves: cree o elija uno (`.pem`) para SSH.
6. Security Group (firewall):

   | Tipo | Puerto | Origen | Para qué |
   |---|---|---|---|
   | SSH | 22 | Su IP (`My IP`) | Entrar a la máquina |
   | TCP personalizado | **8501** | `0.0.0.0/0` | GUI pública, **sin contraseña** |

7. Disco: 8–16 GB llega.
8. *Launch*. Anote la **IPv4 pública**.

### 2.2 Instalar Docker en la instancia

SSH (Windows PowerShell, con la ruta a su `.pem`):

```powershell
ssh -i "C:\ruta\su-clave.pem" ec2-user@IP-PUBLICA
```

En Ubuntu el usuario suele ser `ubuntu`, no `ec2-user`.

**Amazon Linux 2023:**

```bash
sudo dnf update -y
sudo dnf install -y docker
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
exit
```

Vuelva a entrar por SSH (para que el grupo `docker` aplique).

**Ubuntu:**

```bash
sudo apt-get update
sudo apt-get install -y docker.io
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
exit
```

### 2.3 Correr la imagen

```bash
docker pull andresperez3/bohr-h-andresdperezc:0.1.0
docker run -d --restart unless-stopped --name bohr-gui \
  -p 8501:8501 \
  andresperez3/bohr-h-andresdperezc:0.1.0
docker logs -f bohr-gui
```

La imagen ya arranca Streamlit en `0.0.0.0:8501`. Si usara
`localhost` dentro del contenedor, la IP pública no mostraría nada.

Abra en el navegador:

```text
http://IP-PUBLICA:8501
```

No hay usuario ni contraseña. Cualquiera con la IP puede usar la app.
No hay datos personales, pero **no conviene dejarla 24/7** si no se está
mostrando: en la consola EC2, *Instance state → Stop instance*.

Para apagar el contenedor sin parar la VM:

```bash
docker stop bohr-gui
```

### 2.4 Problemas habituales

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| El navegador no carga | Puerto 8501 cerrado en el Security Group | Regla TCP 8501 a `0.0.0.0/0` |
| Tiempo de espera / conexión rechazada | La instancia está *stopped* o Docker no corre | *Start instance*; `sudo systemctl start docker` |
| Carga en localhost de la VM pero no desde casa | Streamlit no escucha en `0.0.0.0` | Use esta imagen; no cambie el `CMD` |
| IP cambió al reiniciar | EC2 asigna otra IPv4 | Use Elastic IP (puede tener costo) o anote la nueva |
| Poco RAM / la app se mata | t2.micro con 1 GB, justo | Cierre otros contenedores; la app de Bohr cabe |

HTTPS (candado verde) no está en este taller: se usa HTTP.

## 3. GitHub Pages (documentación Sphinx)

El flujo de trabajo ya está en `.github/workflows/pages.yml`. Lo activa el autor:

1. Cree el repositorio en GitHub y suba el proyecto (`main`).
2. *Settings → Pages → Source: **GitHub Actions***.
3. Cada push a `main` construye Sphinx y publica el HTML.

URL típica: `https://<usuario>.github.io/<repositorio>/`.

**A mano** (si no usa Actions): genere HTML localmente y súbalo a la rama
`gh-pages`. Incluya un archivo vacío `.nojekyll` para que GitHub no ignore
`_static`:

```powershell
python -m pip install -e ".[docs]"
sphinx-build -b html docs docs/_build/html
```

PDF local (sin LaTeX):

```powershell
sphinx-build -b rinoh docs docs/_build/rinoh
```

El PDF queda en `docs/_build/rinoh/bohr-h-andresdperezc.pdf`.

## 4. Orden recomendado el día de la entrega

1. `pytest -v`
2. TestPyPI → PyPI (`PUBLICAR_PYPI.md`)
3. `docker push` a `andresperez3`
4. GitHub + Pages
5. EC2 solo si va a mostrar la GUI por IP pública; apáguela después
