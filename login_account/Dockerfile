# Use official Node.js base image
FROM node:lts-alpine

# Create app directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build the app
RUN npm run build

# Install serve globally, expose port 80, and serve
RUN npm install -g serve
EXPOSE 80

# CMD to start the server
CMD [ "serve", "-s", "dist", "-l", "80" ]
