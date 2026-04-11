// src/infrastructure/resilience/circuitBreaker.js
const CircuitBreaker = require('opossum');

// আপনার আসল AI ফাংশন যেটা কল হতে সময় লাগতে পারে বা ফেইল করতে পারে
const callExternalAIEngine = async (data) => {
    // Simulated AI API Call
    return new Promise((resolve, reject) => {
        setTimeout(() => resolve({ riskScore: 45 }), 1000);
    });
};

const breakerOptions = {
    timeout: 3000, // ৩ সেকেন্ডের বেশি লাগলে টাইমআউট
    errorThresholdPercentage: 50, // ৫০% রিকোয়েস্ট ফেইল করলে সার্কিট ওপেন হবে
    resetTimeout: 10000 // ১০ সেকেন্ড পর আবার ট্রাই করবে
};

const aiCircuitBreaker = new CircuitBreaker(callExternalAIEngine, breakerOptions);

// যদি AI সার্ভিস ফেইল করে, তাহলে এই ফলব্যাক রান করবে (সিস্টেম ক্র্যাশ করবে না)
aiCircuitBreaker.fallback((data) => {
    console.log("⚠️ AI Engine Down! Using Fallback Rules.");
    return { riskScore: 50, isFallback: true }; 
});

module.exports = { aiCircuitBreaker };
