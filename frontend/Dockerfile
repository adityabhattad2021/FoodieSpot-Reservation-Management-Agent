FROM node:18-alpine 
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

ARG VITE_CHAT_URL

ARG VITE_CHAT_URL $VITE_CHAT_URL

ARG VITE_BACKEND_URL

ENV VITE_BACKEND_URL $VITE_BACKEND_URL

RUN npm run build
EXPOSE 3000
CMD ["npm","run","preview","--","--host"]