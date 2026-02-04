FROM node:18-alpine

WORKDIR /app

# Install dependencies (caching this layer)
COPY package.json .
RUN npm install

# Copy source
COPY . .

# Expose Vite port
EXPOSE 5173

# Run dev server
CMD ["npm", "run", "dev", "--", "--host"]
