FROM node:18-alpine AS base

# Install dependencies only when needed
FROM base AS deps
# Check https://github.com/nodejs/docker-node/tree/b4117f9333da4138b03a546ec926ef50a31506c3#nodealpine to understand why libc6-compat might be needed.
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Install dependencies based on the preferred package manager
# COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* ./
COPY ./web/package.json ./web/yarn.lock* ./web/package-lock.json* ./web/pnpm-lock.yaml* ./

RUN \
  if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
  elif [ -f package-lock.json ]; then npm ci; \
  elif [ -f pnpm-lock.yaml ]; then yarn global add pnpm && pnpm i --frozen-lockfile; \
  else echo "Lockfile not found." && exit 1; \
  fi


# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
# COPY --from=deps ./web/node_modules ./node_modules
COPY ./web .

# Next.js collects completely anonymous telemetry data about general usage.
# Learn more here: https://nextjs.org/telemetry
# Uncomment the following line in case you want to disable telemetry during the build.
# ENV NEXT_TELEMETRY_DISABLED 1

RUN yarn build

# If using npm comment out above and use below instead
# RUN npm run build

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production
# Uncomment the following line in case you want to disable telemetry during runtime.
# ENV NEXT_TELEMETRY_DISABLED 1

ENV USER_ID=1001
ENV GROUP_ID=1001
ENV USER_NAME=nextjs
ENV GROUP_NAME=nodejs

RUN addgroup --system --gid ${GROUP_ID} ${GROUP_NAME}
RUN adduser --system --uid ${USER_ID} ${USER_NAME}

COPY --from=builder /app/public ./public

# Set the correct permission for prerender cache
# USER ${USER_NAME}
RUN mkdir .next
RUN chown -R ${USER_NAME}:${GROUP_NAME} .next

# USER ${USER_NAME}

# Automatically leverage output traces to reduce image size
# https://nextjs.org/docs/advanced-features/output-file-tracing

# COPY --from=builder --chown=${USER_NAME}:${GROUP_NAME} /app/.next/standalone ./
COPY --from=builder --chown=${USER_NAME}:${GROUP_NAME} /app/.next/static ./.next/static

# USER nextjs
USER root
# USER ${USER_NAME}

EXPOSE 3000

ENV PORT 3000
# set hostname to localhost
ENV HOSTNAME "0.0.0.0"

# CMD ["node", "server.js"]
CMD ["npm", "run", "dev"]
