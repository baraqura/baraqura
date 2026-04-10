require('dotenv').config();
const app = require('./src/app.js');
const mongoose = require('mongoose');

const PORT = process.env.PORT || 5000;

// Database Connection
mongoose.connect(process.env.MONGO_URI)
    .then(() => {
        console.log('✅ Connected to MongoDB (V10 Sentinel Core)');
        app.listen(PORT, () => {
            console.log(`🚀 Sentinel Engine Running on Port ${PORT}`);
        });
    })
    .catch(err => {
        console.error('❌ Database Connection Error:', err);
    });
