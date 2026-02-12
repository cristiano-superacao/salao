# Barber & Beauty Scheduler (Streamlit)

Sistema de agendamento online para barbearias e saloes de beleza, agora em Streamlit.

## Requisitos

- Python 3.11+
- Postgres (Railway)

## Configuracao

1. Crie um Postgres no Railway e copie o `DATABASE_URL`.
2. Crie um arquivo `.env` com a variavel `DATABASE_URL` (veja `.env.example`).
3. Instale dependencias:

```bash
pip install -r requirements.txt
```

4. Rode o seed:

```bash
python seed.py
```

5. Inicie o Streamlit:

```bash
streamlit run app.py
```

## Testes

```bash
python scripts/smoke_test.py
```

## Deploy no Railway

- O deploy usa `nixpacks.toml`.
- Certifique-se de definir `DATABASE_URL` nas variaveis do Railway.

Obs: o projeto usa recursos de UI do Streamlit mais recentes (ex.: `type="primary"` em botoes), entao mantenha o `requirements.txt` atualizado.

## Legacy

Os arquivos do site estatico anterior estao em `legacy/`.
