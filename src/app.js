const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const tenantResolver = require('./middlewares/tenantResolver');

const app = express();

app.use(helmet());
app.disable('x-powered-by');
app.use(cors());
app.use(express.json());

// হেলথ চেক (এটি গেটকিপারের বাইরে থাকবে যাতে Vercel চেক করতে পারে)
app.get('/health', (req, res) => {
    res.status(200).json({ status: 'active', engine: 'V10-Sentinel' });
});

// মেইন গেটকিপার বসানো (নিচের সব রুট এখন প্রোটেক্টেড)
app.use(tenantResolver);

// একটি টেস্ট রুট (শুধুমাত্র ভ্যালিড ক্লায়েন্টরা এটি দেখতে পাবে)
app.get('/api/v1/verify', (req, res) => {
    res.status(200).json({
        message: `Welcome ${req.tenant.name}! Your ${req.tenant.plan} plan is active.`,
        tenantId: req.tenant._id
    });
});

module.exports = app;
