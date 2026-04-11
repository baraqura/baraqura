// src/infrastructure/queue/aiQueue.js
const { Queue, Worker } = require('bullmq');
const Redis = require('ioredis');

// Redis Connection
const redisConnection = new Redis(process.env.REDIS_URL || 'redis://127.0.0.1:6379');

// Queue তৈরি করা
const aiProcessQueue = new Queue('AI_PROCESS_QUEUE', { connection: redisConnection });

// Worker তৈরি করা (যে ব্যাকগ্রাউন্ডে কাজ করবে)
const aiWorker = new Worker('AI_PROCESS_QUEUE', async (job) => {
    const { tenantId, payload } = job.data;
    
    console.log(`Processing AI Check for tenant: ${tenantId}`);
    // এখানে আপনার আসল AI Engine কল হবে
    // await runAIEngine(payload);
    
    return { status: "success", risk: 20 };
}, { connection: redisConnection });

module.exports = { aiProcessQueue };
