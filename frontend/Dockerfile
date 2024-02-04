FROM node:21-slim

# Creating working directory
WORKDIR /usr/src/dashboard

# Copy content
COPY . .

RUN npm install

ENTRYPOINT ["npm", "start"]