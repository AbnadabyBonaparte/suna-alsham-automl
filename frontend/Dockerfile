# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install all dependencies for build
RUN npm ci --only=production=false --no-audit --no-fund

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage - ultra minimal
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production

# Install dumb-init for proper signal handling
RUN apk add --no-cache dumb-init

# Create app user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Copy package files
COPY --chown=nextjs:nodejs package*.json ./

# Install only production dependencies
RUN npm ci --only=production --no-audit --no-fund --prefer-offline && \
    npm cache clean --force

# Copy Next.js build output from builder stage
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
COPY --from=builder --chown=nextjs:nodejs /app/public ./public

# Clean up any remaining cache and temp files
RUN rm -rf /tmp/* /var/cache/apk/* && \
    find /usr/local -name "*.md" -delete 2>/dev/null || true

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV NEXT_TELEMETRY_DISABLED=1

# Use dumb-init to handle signals properly
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "server.js"]
