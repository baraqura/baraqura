const Tenant = require('../models/Tenant');

const tenantResolver = async (req, res, next) => {
    const apiKey = req.headers['x-api-key'];
    const apiSecret = req.headers['x-api-secret'];

    // ১. Vercel-এ সেভ করা আপনার Master Key চেক করা
    // ধরে নিচ্ছি Vercel-এ আপনার Key-র নাম MASTER_API_KEY এবং Secret-এর নাম MASTER_API_SECRET
    const masterKey = process.env.MASTER_API_KEY; 
    const masterSecret = process.env.MASTER_API_SECRET;

    if (apiKey === masterKey && apiSecret === masterSecret) {
        // আপনি মাস্টার কি দিয়েছেন, তাই সরাসরি এক্সেস!
        req.tenant = { name: "Supreme Leader (Admin)", plan: "god-mode", _id: "admin-001" };
        return next();
    }

    // ২. যদি মাস্টার কি না মেলে, তবে চেক করো ডাটাবেজে কোনো ক্লায়েন্ট আছে কি না
    if (!apiKey || !apiSecret) {
        return res.status(401).json({ error: 'Authentication failed. API Key and Secret are required.' });
    }

    try {
        const tenant = await Tenant.findOne({ apiKey, apiSecret, isActive: true });

        if (!tenant) {
            return res.status(403).json({ error: 'Invalid or Inactive API Credentials.' });
        }

        req.tenant = tenant;
        next();
    } catch (error) {
        res.status(500).json({ error: 'Internal Server Error in Gatekeeper.' });
    }
};

module.exports = tenantResolver;
