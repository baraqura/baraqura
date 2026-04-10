const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const morgan = require('morgan');

const app = express();

// Security Layer 1: Helmet দিয়ে হেডার প্রটেকশন
app.use(helmet());

// Security Layer 2: Metadata রিমুভাল
app.disable('x-powered-by');

app.use(cors());
app.use(express.json({ limit: '10kb' })); // Payload size limit
app.use(morgan('dev'));

// Health Check Endpoint
app.get('/health', (req, res) => {
    res.status(200).json({ status: 'active', timestamp: new Date() });
});

module.exports = app;
