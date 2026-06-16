# reference

## scan wifi network

    sudo arp-scan --interface=wlan0 --localnet

## ollama commands

### ollama service

    systemctl start ollama
    systemctl status ollama
    systemctl stop ollama

### view ollama service startup log to debug

    journalctl -u ollama -n 50 --no-pager

### docker

    docker exec -ti ollama ls -al /root/.ollama    
    docker exec -ti ollama ollama list
    docker exec -ti ollama ollama pull qwen3.6:35b

## location of ollama files

    /root/.ollama

## .ssh file and folder privileges

    .ssh folder           700         owner can read, write and exec, for permissions for group and others 
    private key files     600         only owner can read and write
    public key files      644         owner can read and write, group can read, others can read

## alpine linux

### configure ssh access for existing user

from local machine, copy ssh-public-key to remote server, for existing user

    ssh-copy-id -i ~/.ssh/solomon.id_ed25519.pub solomon@jebel

### upgrade existing user to root

    # install doas util
    apk add doas

    # add user solomon to wheel group
    adduser solomon wheel

    # Configure doas to permit wheel group members to run commands as root
    echo 'permit :wheel as root' > /etc/doas.d/doas.conf
