const Tenant = require('../models/Tenant');

const tenantResolver = async (req, res, next) => {
    // হেডার থেকে API Key এবং Secret রিড করা
    const apiKey = req.headers['x-api-key'];
    const apiSecret = req.headers['x-api-secret'];

    // ১. চাবি আছে কি না চেক করা
    if (!apiKey || !apiSecret) {
        return res.status(401).json({
            error: 'Authentication failed. API Key and Secret are required.'
        });
    }

    try {
        // ২. ডাটাবেজে এই চাবিওয়ালা কোনো ক্লায়েন্ট আছে কি না দেখা
        const tenant = await Tenant.findOne({ apiKey, apiSecret, isActive: true });

        if (!tenant) {
            return res.status(403).json({
                error: 'Invalid or Inactive API Credentials.'
            });
        }

        // ৩. রিকোয়েস্ট অবজেক্টে টেন্যান্টকে সেভ করা (যাতে পরে ব্যবহার করা যায়)
        req.tenant = tenant;
        next(); // সব ঠিক থাকলে পরের ধাপে যাও
    } catch (error) {
        res.status(500).json({ error: 'Internal Server Error in Gatekeeper.' });
    }
};

module.exports = tenantResolver;
