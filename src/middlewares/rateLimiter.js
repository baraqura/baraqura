// এই মিডলওয়্যারটি চেক করবে একজন ইউজার ১ মিনিটে কয়টা রিকোয়েস্ট করছে
const rateLimit = {}; // আপাতত ইন-মেমোরি (পরবর্তীতে আমরা রেডিস ব্যবহার করবো)

const rateLimiter = (req, res, next) => {
    const tenantId = req.tenant._id;
    const currentTime = Date.now();
    
    // প্রতি প্ল্যানের জন্য আলাদা লিমিট
    const limits = {
        'free': 10,       // ১ মিনিটে ১০টি
        'pro': 100,      // ১ মিনিটে ১০০টি
        'enterprise': 1000, // ১ মিনিটে ১০০০টি
        'god-mode': 999999  // আনলিমিটেড (আপনার জন্য)
    };

    const limit = limits[req.tenant.plan] || 5;

    if (!rateLimit[tenantId]) {
        rateLimit[tenantId] = { count: 1, startTime: currentTime };
        return next();
    }

    const timePassed = (currentTime - rateLimit[tenantId].startTime) / 1000;

    if (timePassed < 60) {
        if (rateLimit[tenantId].count >= limit) {
            return res.status(429).json({ 
                error: 'Too many requests.', 
                message: `Your ${req.tenant.plan} plan allows only ${limit} requests per minute.` 
            });
        }
        rateLimit[tenantId].count++;
    } else {
        rateLimit[tenantId] = { count: 1, startTime: currentTime };
    }

    next();
};

module.exports = rateLimiter;
