// src/middlewares/tenantResolver.js

const tenantResolver = async (req, res, next) => {
    try {
        // ১. হেডার থেকে API Key নেওয়া
        const apiKey = req.headers['x-api-key'];
        
        if (!apiKey) {
            return res.status(401).json({ error: "API Key missing" });
        }

        // ২. রিয়েল ডাটাবেস কানেকশন (ভবিষ্যতের জন্য রেডি রাখা হলো)
        // const tenant = await TenantModel.findOne({ apiKey });

        // ৩. আপাতত টেস্টিংয়ের জন্য ডামি টেনান্ট কনটেক্সট
        const tenant = {
            id: "tenant_123",
            plan: "pro", // 'free', 'pro', বা 'enterprise'
            limits: 5000, // planLimit
            currentUsage: 1500, // Billing layer চেক করার জন্য
            status: "active", // 'active', 'past_due', 'canceled'
            riskProfile: "normal"
        };

        if (!tenant) {
            return res.status(403).json({ error: "Invalid API Key" });
        }

        // ৪. গ্লোবাল কনটেক্সট সেট করা হলো (যাতে পুরো সিস্টেম এটাকে চিনতে পারে)
        req.tenant = tenant;
        
        next();

    } catch (error) {
        next(error);
    }
};

module.exports = tenantResolver;
