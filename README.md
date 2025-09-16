# Discord KeyAuth Bot

Bot de Discord que integra com a Seller API do KeyAuth. Implementa operações comuns via slash commands.

Observação: os parâmetros `type` e nomes de campos podem variar conforme a documentação atual do KeyAuth. Verifique a documentação oficial da Seller API e ajuste se necessário em `keyauth_api.py`.

## Recursos
- Slash commands com `discord.py` 2.x
- Wrapper `KeyAuthAPI` para: criação de chaves, info, ban, unban, reset HWID e exclusão
- Estrutura em Cogs e variáveis de ambiente

## Pré‑requisitos
- Python 3.10+
- Bot do Discord (token ativo)
- Seller Key do KeyAuth

## Configuração
1. Copie `.env.example` para `.env` e preencha:
   - `DISCORD_TOKEN`
   - `DEV_GUILD_ID` (opcional para sync rápido)
   - `KEYAUTH_SELLER_URL` (padrão `https://keyauth.win/api/seller/`)
   - `KEYAUTH_SELLER_KEY`

2. Instale dependências:
   ```bash
   python -m venv .venv && . .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Execute:
   ```bash
   python bot.py
   ```

## Comandos
Grupo `/kauth`:
- `/kauth info key:<texto>` — Consulta dados de uma key
- `/kauth gerar amount:<int> [expiry_days] [level]` — Cria `amount` chaves com validade e nível informados
- `/kauth ban key:<texto>` — Bane a key
- `/kauth unban key:<texto>` — Desbane a key
- `/kauth reset key:<texto>` — Reseta HWID da key
- `/kauth deletar key:<texto>` — Exclui a key

Permissões: por padrão, somente administradores do servidor. Edite `utils/checks.py` para permitir usuários específicos.

## Estrutura
```
discord-keyauth-bot/
├─ .gitignore
├─ .env.example
├─ README.md
├─ requirements.txt
├─ LICENSE
├─ bot.py
├─ keyauth_api.py
├─ utils/
│  └─ checks.py
└─ cogs/
   └─ licenses.py
```

## Ajustes na API
A Seller API do KeyAuth aceita parâmetros via querystring e/ou formulário. Este projeto envia como `application/x-www-form-urlencoded`. Caso a API mude, atualize o método `request()` em `keyauth_api.py` para adequar.