FROM node:18-alpine

WORKDIR /app

# Copy package.json and install dependencies
COPY package.json package-lock.json* ./
RUN npm install

# Copy source code
COPY . .

# Build the app (if needed for production, else just run dev server for port 3000 mapping)
# Actually, Vite dev server by default runs on 5173, but let's use it for development here
# and expose the port
EXPOSE 3000

# We use host 0.0.0.0 to allow external access
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]
