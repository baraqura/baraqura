const app = require('./src/app.js');
const mongoose = require('mongoose');

const PORT = process.env.PORT || 5000;

// Database Connection
mongoose.connect(process.env.MONGO_URI)
    .then(() => {
        console.log('✅ Connected to MongoDB');
        app.listen(PORT, () => {
            console.log(`🚀 Sentinel Running on Port ${PORT}`);
        });
    })
    .catch(err => console.error('❌ DB Error:', err));
