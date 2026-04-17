# ── Stage 1: build ────────────────────────────────────────────────────────
FROM node:20-bookworm-slim AS build

WORKDIR /app
ENV NODE_ENV=development

ARG VITE_API_BASE=/api/v1
ENV VITE_API_BASE=$VITE_API_BASE

COPY package.json package-lock.json* ./
RUN npm config set fund false \
	&& npm config set audit false \
	&& npm config set update-notifier false \
	&& npm config set strict-ssl false \
	&& npm cache clean --force \
	&& (if [ -f package-lock.json ]; then npm ci --include=dev --loglevel=verbose; else npm install --include=dev --loglevel=verbose; fi \
		|| npm install --include=dev --legacy-peer-deps --loglevel=verbose) \
	&& npm install --no-save --loglevel=verbose @rollup/rollup-linux-x64-gnu \
	&& test -x node_modules/.bin/vite

COPY . .
RUN npm run build

# ── Stage 2: serve with nginx ─────────────────────────────────────────────
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
