# 使用 Node.js 官方映像
FROM node:lts-alpine

# 設定工作目錄
WORKDIR /app

# 複製 package.json 和 package-lock.json
COPY package*.json ./

# 安裝依賴
RUN npm install

# 複製代碼到容器
COPY . .

# 預設執行生產模式
RUN npm run build

# 安裝 serve 作為全域套件
RUN npm install -g serve
EXPOSE 80

# 使用 serve 啟動靜態服務器
CMD ["npx", "serve", "-s", "dist", "-l", "80"]
