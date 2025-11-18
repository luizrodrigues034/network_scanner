# 🛡️ Python Port Scanner

Um scanner de portas simples, multi-thread e eficiente escrito em Python 3. Esta ferramenta permite verificar portas abertas em um host alvo (IP ou domínio), realizar resolução de DNS e capturar banners de serviços HTTP.

## 🚀 Funcionalidades

- **Multi-threading:** Escaneamento rápido utilizando múltiplas threads simultâneas.
- **Resolução de DNS:** Resolve nomes de domínio para IP automaticamente.
- **DNS Reverso:** Opção para resolver IPs de volta para nomes de host (`-R`).
- **Seleção Flexível de Portas:**
  - Lista separada por vírgulas (ex: `80,443,8080`).
  - Intervalos de portas (ex: `1-1000`).
  - Arquivo padrão de portas web comuns (se nenhum argumento for passado).
- **Banner Grabbing:** Tenta capturar o banner do serviço (HTTP HEAD) em portas abertas.
- **Output Colorido:** Visualização facilitada do status das portas.
- **Métricas:** Exibe o tempo total de execução ao final.

## 📋 Pré-requisitos

Para executar este script, você precisará de:

- Python 3.x
- Biblioteca `regex` (biblioteca externa)

### Instalação das Dependências

O script utiliza a biblioteca `regex`. Você pode instalá-la via pip:

```bash
pip install regex
```

Exemplos
```
python3 scanner.py -H 192.168.1.15 -P 22,80,443,3306

python3 scanner.py -H scanme.nmap.org -P 1-1000

python3 scanner.py -H 8.8.8.8 -P 53 -R