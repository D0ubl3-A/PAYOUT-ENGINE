FROM node:20-slim

WORKDIR /app

COPY package.json .
COPY tsconfig.json .
COPY next.config.js .
COPY next-env.d.ts .

RUN corepack enable && pnpm install

COPY src ./src

RUN pnpm build

EXPOSE 3000
CMD ["pnpm", "start", "-p", "3000"]
