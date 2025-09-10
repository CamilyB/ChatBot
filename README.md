## 📝 Sistema Automatizado de Verificação do Código de Normas de Santa Catarina

Este projeto está em desenvolvimento como parte de um projeto de extensão da minha faculdade.
A proposta é criar um chatbot integrado ao Microsoft Teams que será capaz de verificar automaticamente o Código de Normas de Santa Catarina e informar:
- Se houve alterações em artigos existentes.
- Se foram adicionados novos artigos.
- Quais artigos foram impactados pelo último Provimento.

Dessa forma, o chatbot informará diretamente no Teams as últimas alterações normativas, sem a necessidade de verificação manual diária e evitando erros jurídicos.

## ⚙️ Funcionalidades já implementadas

📥 Download automático do PDF mais recente do Código de Normas de SC.

🔍 Comparação entre versões para verificar se houve atualização.

🗑️ Limpeza automática dos PDFs após a verificação (não acumula arquivos locais).

📑 Identificação de artigos impactados pelo último provimento publicado (pesquisa por "Provimento n. XX", com ou sem espaço).

## 📚 Tecnologias e Bibliotecas Utilizadas

- Python 3 → Linguagem principal do projeto.
- Requests → Requisições HTTP para baixar os arquivos.
- BeautifulSoup (bs4) → Extração dos links do TJSC.
- PyPDF2 → Leitura e manipulação de PDFs.
- difflib → Comparação entre versões do documento.
- OS / Shutil → Manipulação de arquivos locais.
- Git/GitHub → Controle de versão e colaboração.

## 🚀 Próximos Passos (Roadmap)

🤖 Transformar em Chatbot: integração ao Microsoft Teams para interação em linguagem natural.

📩 Respostas automáticas: permitir que o usuário pergunte "quais foram as últimas alterações?" e receba a lista atualizada.

📊 Resumo detalhado das mudanças em formato legível (texto/markdown).

🕒 Agendamento automático para rodar diariamente.

☁️ Hospedagem em nuvem para manter o bot ativo 24/7.

## 👩‍💻 Status

🔨 Projeto em desenvolvimento

O sistema já consegue baixar, comparar e identificar alterações. O próximo grande passo é a integração com o Microsoft Teams para uso como chatbot.
