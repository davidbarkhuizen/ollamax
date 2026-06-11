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


'
docker exec -ti ollama ls -al /root/.ollama

docker exec -ti ollama ollama list
docker exec -ti ollama ollama pull qwen3.6:35b
