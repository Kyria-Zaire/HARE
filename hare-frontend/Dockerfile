# HARE Pro v2.0 – Frontend (multi-stage, nginx non-root)
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
RUN echo 'server { listen 8080; gzip on; location / { try_files $uri $uri/ /index.html; } }' > /etc/nginx/conf.d/default.conf
RUN addgroup -g 1001 nginxgroup && adduser -u 1001 -G nginxgroup -D nginxuser \
    && chown -R nginxuser:nginxgroup /usr/share/nginx/html /var/cache/nginx /var/run /etc/nginx/conf.d
USER nginxuser
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
