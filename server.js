require('dotenv').config(); // Vercel থেকে env পড়ার জন্য
const mongoose = require('mongoose');
const app = require('./src/app.js');

const PORT = process.env.PORT || 5000;
const MONGO_URI = process.env.MONGO_URI;

// DB Options for stability
const dbOptions = {
    useNewUrlParser: true,
    useUnifiedTopology: true
};

mongoose.connect(MONGO_URI, dbOptions)
    .then(() => {
        console.log('✅ Connected to MongoDB');
        if (process.env.NODE_ENV !== 'test') {
            app.listen(PORT, () => console.log(`🚀 Sentinel Engine Running on Port ${PORT}`));
        }
    })
    .catch(err => console.error('❌ MongoDB Connection Error:', err));
