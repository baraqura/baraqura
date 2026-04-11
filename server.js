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

// ৩. Health Check Route (সিস্টেমের হার্টবিট - এটি DB কানেকশনের আগেই রাখা ভালো)
app.get('/health', (req, res) => {
    res.json({
        status: "UP",
        uptime: process.uptime(),
        memoryUsage: process.memoryUsage(),
        timestamp: new Date().toISOString()
    });
});

// ৪. Database Connection
const dbOptions = {};

mongoose.connect(MONGO_URI, dbOptions)
    .then(() => {
        console.log('✅ Connected to MongoDB');
        
        // ৫. Routes & Pipeline
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

        // ৬. Server Start
        app.listen(PORT, () => {
            console.log(`🚀 V10 Sentinel Empire Live on Port ${PORT}`);
        });
    })
    .catch(err => {
        console.error('❌ MongoDB Connection Error:', err);
        process.exit(1); 
    });

module.exports = app;
