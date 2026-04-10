const mongoose = require('mongoose');

const tenantSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true,
        trim: true
    },
    apiKey: {
        type: String,
        required: true,
        unique: true
    },
    apiSecret: {
        type: String,
        required: true
    },
    plan: {
        type: String,
        enum: ['free', 'pro', 'enterprise'],
        default: 'free'
    },
    isActive: {
        type: Boolean,
        default: true
    },
    createdAt: {
        type: Date,
        default: Date.now
    }
});

// ইনডেক্সিং (দ্রুত ডাটা খুঁজে পাওয়ার জন্য এবং সিকিউরিটির জন্য)
tenantSchema.index({ apiKey: 1 });

module.exports = mongoose.model('Tenant', tenantSchema);
