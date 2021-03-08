FROM node:14-alpine

RUN apk add git make

ADD src/ /app
WORKDIR /app

RUN npm install && \
    npm run all

CMD ["npm", "start"]
