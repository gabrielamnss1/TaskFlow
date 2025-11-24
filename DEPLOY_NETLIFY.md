# 🚀 Como fazer Deploy no Netlify

Este guia explica como fazer o deploy do TaskFlow no Netlify.

## 📋 Pré-requisitos

- Conta no [Netlify](https://www.netlify.com/) (gratuita)
- Repositório no GitHub com o código do projeto

## 🔧 Passo a Passo

### 1. Faça login no Netlify

Acesse [https://app.netlify.com/](https://app.netlify.com/) e faça login com sua conta GitHub.

### 2. Importe o Projeto

1. Clique em **"Add new site"** → **"Import an existing project"**
2. Escolha **"Deploy with GitHub"**
3. Autorize o Netlify a acessar seus repositórios
4. Selecione o repositório **projeto_W** ou **TaskFlow**

### 3. Configure o Deploy

Na página de configuração, use estas opções:

- **Branch to deploy**: `main`
- **Base directory**: deixe em branco
- **Build command**: deixe em branco (não precisa de build)
- **Publish directory**: `public`

### 4. Deploy

1. Clique em **"Deploy site"**
2. Aguarde alguns segundos enquanto o Netlify faz o deploy
3. Seu site estará no ar! 🎉

### 5. Personalize a URL (Opcional)

1. Vá em **"Site settings"** → **"Domain management"**
2. Em **"Custom domain"**, clique em **"Options"** → **"Edit site name"**
3. Escolha um nome único (ex: `taskflow-seunome`)
4. Sua URL será: `https://taskflow-seunome.netlify.app`

## 🌐 Estrutura do Projeto para Netlify

```
TaskFlow/
├── public/              # Pasta que será publicada
│   ├── index.html       # Página principal
│   ├── style.css        # Estilos
│   └── app.js           # Funcionalidades
└── netlify.toml         # Configurações do Netlify
```

## 💾 Como Funciona o Sistema

**TaskFlow** agora é uma aplicação 100% frontend que funciona no navegador:

- **Sem Backend**: Não precisa de servidor Python/Flask
- **LocalStorage**: Dados salvos no navegador do usuário
- **Funcionalidades Completas**:
  - ✅ Cadastro e login de usuários
  - ✅ Criar, editar, concluir e excluir tarefas
  - ✅ Filtros por status (todas, pendentes, concluídas, atrasadas)
  - ✅ Busca por título/descrição
  - ✅ Ordenação (data, prazo, título)
  - ✅ Exportação de dados (JSON, CSV)
  - ✅ Estatísticas e relatórios
  - ✅ Perfil do usuário
  - ✅ Design responsivo (mobile, tablet, desktop)

## ⚠️ Importante

- Os dados são salvos localmente no navegador (localStorage)
- Cada usuário terá seus dados apenas no dispositivo que usar
- Limpar cache/dados do navegador apaga as informações
- Perfeito para uso pessoal ou demonstrações

## 🔄 Atualizações Automáticas

Toda vez que você fizer push para o GitHub:

```bash
git add .
git commit -m "Atualização"
git push projeto_w main
```

O Netlify detecta automaticamente e atualiza o site! ✨

## 🆘 Problemas Comuns

### Site mostrando erro 404
- Verifique se a pasta `public` está configurada como "Publish directory"
- Confirme que `index.html` está dentro de `public/`

### Funcionalidades não funcionam
- Abra o Console do navegador (F12) e verifique erros
- Certifique-se que `app.js` e `style.css` estão sendo carregados

### Deploy falhou
- Verifique se todos os arquivos foram commitados
- Confira se `netlify.toml` está na raiz do projeto

## 📱 Teste Local

Para testar localmente antes do deploy:

```bash
# Opção 1: Usar Live Server no VS Code
# Clique com botão direito em public/index.html → "Open with Live Server"

# Opção 2: Usar Python
cd public
python -m http.server 8000
# Acesse: http://localhost:8000

# Opção 3: Usar Node.js
npx serve public
```

## 🎨 Personalizações

Você pode personalizar cores no arquivo `public/style.css`:

```css
:root {
    --primary-color: #6a4c93;     /* Cor principal */
    --secondary-color: #8b5cf6;    /* Cor secundária */
    --success-color: #10b981;      /* Cor de sucesso */
    --warning-color: #f59e0b;      /* Cor de aviso */
    --danger-color: #ef4444;       /* Cor de perigo */
}
```

## 🌟 Recursos do Layout

- 🎨 **Design Moderno**: Gradientes e sombras suaves
- 📱 **Responsivo**: Adapta-se a qualquer tela
- 🌙 **Profissional**: Interface limpa e organizada
- ⚡ **Rápido**: Carrega instantaneamente
- 🎭 **Animações**: Transições suaves e modais elegantes

---

**Desenvolvido com ❤️ | TaskFlow 2025**
