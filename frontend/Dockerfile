# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copia arquivos de dependências
COPY package*.json ./

# Instala TODAS as dependências (incluindo dev) para o build
RUN npm ci --only=production=false

# Copia o restante do código do frontend
COPY . .

# Build de produção
RUN npm run build

# Production stage
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production

# Create app user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy built application
COPY --from=builder /app/public ./public
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# Install only production dependencies
RUN npm ci --only=production && npm cache clean --force

USER nextjs

ENV PORT=3000
EXPOSE 3000

CMD ["node", "server.js"]
