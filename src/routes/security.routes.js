// src/routes/security.routes.js
const express = require('express');
const router = express.Router();

// ইমপোর্টস
const tenantResolver = require('../middlewares/tenantResolver');
const { aiProcessQueue } = require('../infrastructure/queue/aiQueue');
const { aiCircuitBreaker } = require('../infrastructure/resilience/circuitBreaker');
const { evaluateFinalAction } = require('../core/ai/guardrail');

// রাউট: POST /api/v1/protect
router.post('/protect', tenantResolver, async (req, res) => {
    try {
        const payload = req.body;
        const tenant = req.tenant;

        // ১. Async Logging/Billing এর জন্য Queue তে পাঠানো (API ব্লক করবে না)
        await aiProcessQueue.add('log-request', {
            tenantId: tenant.id,
            payload
        });

        // ২. Circuit Breaker দিয়ে AI কল করা (ফেইল সেফ)
        const aiResult = await aiCircuitBreaker.fire(payload);

        // ৩. Guardrail দিয়ে ফাইনাল ডিসিশন নেওয়া
        const finalAction = evaluateFinalAction(aiResult, tenant);

        // ৪. রেসপন্স
        if (finalAction === 'BLOCK') {
            return res.status(403).json({ error: "Access Denied by Sentinel" });
        }

        res.status(200).json({ 
            status: "allowed", 
            action: finalAction,
            riskScore: aiResult.riskScore 
        });

    } catch (error) {
        console.error("Pipeline Error:", error);
        res.status(500).json({ error: "Internal System Error" });
    }
});

module.exports = router;
