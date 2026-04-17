# ── Stage 1: build ────────────────────────────────────────────────────────
FROM node:20-alpine AS build

WORKDIR /app
ENV NODE_ENV=development
ENV NPM_CONFIG_PRODUCTION=false

ARG VITE_API_BASE=/api/v1
ENV VITE_API_BASE=$VITE_API_BASE

COPY package.json package-lock.json* ./
RUN if [ -f package-lock.json ]; then npm ci --include=dev --omit=optional; else npm install --include=dev --omit=optional; fi \
	&& test -x node_modules/.bin/vite

COPY . .
RUN npm run build

# ── Stage 2: serve with nginx ─────────────────────────────────────────────
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
