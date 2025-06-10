# Base image
FROM node:18

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy package.json và package-lock.json
COPY package*.json ./

# Cài đặt dependencies
RUN npm install

# Cài đặt Angular CLI
RUN npm install -g @angular/cli

# Copy source code
COPY . .

# Build và serve ứng dụng
EXPOSE 4200
CMD ["ng", "serve", "--host", "0.0.0.0", "--disable-host-check"] 