# Instalando Geocoder

## Dependencias
- Docker
- Redis
- Pyenv
- python >= 3.10.12

## Instalación de docker

1. Limipiar versiones antiguas y paquetes obsoletos:
```bash
        for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

2. Agregue la clave GPG oficial de Docker:
```bash
        sudo apt-get update
```
```bash
        sudo apt-get install ca-certificates curl
```
```bash
        sudo install -m 0755 -d /etc/apt/keyrings
```
```bash
        sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
```
```bash
        sudo chmod a+r /etc/apt/keyrings/docker.asc
```

3. Agregue el repositorio a las fuentes de Apt:
```bash
        echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
        $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
        sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
```bash
        sudo apt-get update
```
4. Lista las versiones disponibles:
```bash
        sudo apt-cache madison docker-ce | awk '{ print $3 }'
```

5. Select the desired version and install:
```bash
        VERSION_STRING=5:27.0.3-1~ubuntu.24.04~noble
```
```bash
        sudo apt-get install docker-ce=$VERSION_STRING docker-ce-cli=$VERSION_STRING containerd.io docker-buildx-plugin docker-compose-plugin 
```

6. Verificar la instalacion:
```bash
        docker –version
```


## Instalación de Redis
1. Ejecutar el comando:
```bash
        docker compose -f docker-compose-redis.yml up -d
```
2. Verificar instalacion:
```bash
        docker ps -a
```
2. Ver el log del contenedor
```bash
        docker logs -f redis-geocoder
```

## Instalación de pyenv e instalacion de Python 3.10.12
1. Instalar y actualizar las dependencias
```bash
        sudo apt update -y
```
```bash
        sudo apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
```
2. En este paso, debe descargar el script de Pyenv en Ubuntu
```bash
        curl https://pyenv.run | bash
```
3. Configurar el entorno
```bash
        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
```
```bash
        echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
```
```bash
        echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init -)"\nfi' >> ~/.bashrc
```
4. Finalmente, reinicie el shell ejecutando: para comenzar a utilizar pyenv.
```bash
        exec "$SHELL"
```
5. Revise la instalación
```bash
        pyenv install --list
```
6. Instalar Python Ver. 3.10.12
```bash
        pyenv install 3.10.12
```
6. Activar Python Ver. 3.10.12
```bash
        pyenv global 3.10.12
```

### Instalar Geocoder
1. Crear el entorno virtual:
```bash
        python -m venv env
```
2. Activar el entorno virtual:
```bash
        source env/bin/activate
```
3. Instalar las dependencias:
```bash
        pip install -r requirements.txt
```

4. Crear el serivicio:
```bash
        nano /etc/systemd/system/geocoder.service
```
5. Pegar el siguiente codigo (reemplazar [path] por tu ruta raiz donde esta el proyecto):
```bash

        [Unit]
        Description=Geocoder
        [Service]
        Type=simple
        SyslogIdentifier=geocoder_py
        PermissionsStartOnly=true
        ExecStart= path/env/bin/python3 path/app.py serve --host 0.0.0.0 --port 3051
        StandardOutput=journal+console
        [Install]
        WantedBy=multi-user.target
```
6. Reiniciar los servicios:
```bash
sudo systemctl daemon-reload
```

7. Activar el servicio del geocoder e iniciarlo:
```bash
sudo systemctl start geocoder.service && sudo systemctl enable geocoder.service
```
8. Verficar el estado del servicio:
```bash
sudo systemctl status geocoder.service
```