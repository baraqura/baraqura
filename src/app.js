const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const tenantResolver = require('./middlewares/tenantResolver');
const rateLimiter = require('./middlewares/rateLimiter');

const app = express();

app.use(helmet());
app.disable('x-powered-by');
app.use(cors());
app.use(express.json());

// ১. হেলথ চেক (সবার জন্য ওপেন)
app.get('/health', (req, res) => {
    res.status(200).json({ status: 'active', engine: 'V10-Sentinel' });
});

// ২. গেটকিপার (ভ্যালিড চাবি ছাড়া ঢোকা নিষেধ)
app.use(tenantResolver);

// ৩. রেট-লিমিট (বেশি জোরে চালালে ব্রেক ধরবে)
app.use(rateLimiter);

// ৪. ভেরিফিকেশন টেস্ট রুট
app.get('/api/v1/verify', (req, res) => {
    res.status(200).json({
        message: `Welcome ${req.tenant.name}! Access Granted.`,
        plan: req.tenant.plan
    });
});

module.exports = app;
