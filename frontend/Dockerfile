FROM node:20-alpine

WORKDIR /app

# Copia arquivos de dependências
COPY package*.json ./

# Instala TODAS as dependências (incluindo dev) para o build
RUN npm ci

# Copia o restante do código do frontend
COPY . .

# Build de produção
RUN npm run build

# Remove dependências de desenvolvimento após build
RUN npm prune --production

ENV PORT=3000
EXPOSE 3000

CMD ["npm", "run", "start"]
