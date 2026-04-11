# ১. নোড ভার্সন সিলেক্ট করা
FROM node:20-alpine

# ২. প্রজেক্ট ফোল্ডার তৈরি
WORKDIR /app

# ৩. শুধু প্যাকেজ ফাইলগুলো আগে কপি করা (Cache optimization এর জন্য)
COPY package*.json ./

# ৪. সব লাইব্রেরি ইনস্টল করা
RUN npm install --production

# ৫. বাকি সব কোড কপি করা
COPY . .

# ৬. পোর্ট এক্সপোজ করা (আমরা ৫০০৩ ব্যবহার করছি)
EXPOSE 5000

# ৭. সার্ভার রান করা
CMD ["npm", "start"]
