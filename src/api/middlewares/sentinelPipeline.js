// src/api/middlewares/sentinelPipeline.js
const { trackUsage } = require('../../infrastructure/billing/orchestrator');
const { aiGuardrail } = require('../../core/ai/guardrail');
const { aiCircuitBreaker } = require('../../infrastructure/resilience/circuitBreaker');
const logger = require('../../infrastructure/logging/logger'); // লগার ইম্পোর্ট করা হলো

const sentinelPipeline = async (req, res, next) => {
    try {
        const tenant = req.tenant;

        // স্টেপ ১: বিলিং চেক (লিমিট আছে তো?)
        try {
            await trackUsage(tenant);
        } catch (err) {
            logger.warn({ event: "BILLING_LIMIT_EXCEEDED", tenantId: tenant.id });
            return res.status(402).json({ error: "Billing limit exceeded. Upgrade your plan." });
        }

        // স্টেপ ২: AI রিস্ক চেক (সার্কিট ব্রেকার দিয়ে)
        const aiResult = await aiCircuitBreaker.fire(req.body);
        
        // স্টেপ ৩: গার্ডরেল দিয়ে সিদ্ধান্ত নেওয়া
        const finalAction = aiGuardrail(aiResult.riskScore, tenant);

        // স্টেপ ৪: লগিং (পর্দার আড়ালে কী হচ্ছে তা রেকর্ড করা)
        logger.info({
            event: "REQUEST_PROCESSED",
            tenantId: tenant.id,
            action: finalAction,
            risk: aiResult.riskScore,
            timestamp: new Date().toISOString()
        });

        // স্টেপ ৫: অ্যাকশন অনুযায়ী রেসপন্স
        if (finalAction === "BLOCK") {
            return res.status(403).json({ 
                error: "Security Block", 
                message: "High risk activity detected by V10 Sentinel." 
            });
        }

        if (finalAction === "CHALLENGE") {
            return res.status(401).json({ 
                status: "challenge_required", 
                message: "Please complete CAPTCHA to proceed." 
            });
        }

        // সবকিছু ঠিক থাকলে পরের ধাপে যাও
        next();

    } catch (error) {
        // যদি AI ইঞ্জিন ফেইল করে, এরর লগ করে সেফলি এলাউ করে দিব (Fail-Open)
        logger.error({ event: "PIPELINE_CRITICAL_ERROR", message: error.message });
        next();
    }
};

module.exports = { sentinelPipeline };
