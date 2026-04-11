require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const tenantResolver = require('./src/middlewares/tenantResolver');
const { sentinelPipeline } = require('./src/api/middlewares/sentinelPipeline');

// ১. App Setup
const app = express();
app.use(express.json());

// ২. Environment Variables
const PORT = process.env.PORT || 5000;
const MONGO_URI = process.env.MONGO_URI;

// ৩. Database Connection
const dbOptions = {
    // useNewUrlParser: true, // নতুন ড্রাইভার ভার্সনে এগুলো অপশনাল, তবে স্ট্যাবিলিটির জন্য রাখা হলো
    // useUnifiedTopology: true
};

mongoose.connect(MONGO_URI, dbOptions)
    .then(() => {
        console.log('✅ Connected to MongoDB');
        
        // ৪. Routes & Pipeline (DB কানেক্ট হওয়ার পর এগুলো অ্যাক্টিভ হবে)
        // সব সিকিউরিটি রাউটের জন্য এই পাইপলাইন কাজ করবে
        app.use('/api/v1/secure', tenantResolver, sentinelPipeline);

        // টেস্ট রাউট
        app.post('/api/v1/secure/data', (req, res) => {
            res.json({ 
                message: "Welcome to the Secure Empire, Boss!", 
                tenant: req.tenant.id,
                status: "Data access granted under V10 Protection" 
            });
        });

        // ৫. Server Start
        app.listen(PORT, () => {
            console.log(`🚀 V10 Sentinel Empire Live on Port ${PORT}`);
        });
    })
    .catch(err => {
        console.error('❌ MongoDB Connection Error:', err);
        process.exit(1); // DB ছাড়া সিস্টেম চলবে না, তাই প্রসেস বন্ধ করে দিবে
    });

module.exports = app; // Vercel বা টেস্টিংয়ের জন্য এক্সপোর্ট রাখা হলো
