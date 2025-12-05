# Ultra-minimal production image
FROM node:20-alpine

WORKDIR /app

ENV NODE_ENV=production

# Install dumb-init for proper signal handling
RUN apk add --no-cache dumb-init

# Create app user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Copy package files first for better caching
COPY --chown=nextjs:nodejs package*.json ./

# Install only production dependencies with minimal footprint
RUN npm ci --only=production --no-audit --no-fund --prefer-offline && \
    npm cache clean --force

# Copy Next.js build output
COPY --chown=nextjs:nodejs .next/standalone ./
COPY --chown=nextjs:nodejs .next/static ./.next/static
COPY --chown=nextjs:nodejs public ./public

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
