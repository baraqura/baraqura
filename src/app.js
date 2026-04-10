const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const morgan = require('morgan');

const app = express();

app.use(helmet()); // সিকিউরিটি হেডার
app.disable('x-powered-by'); // মেটাডেটা হাইড করা
app.use(cors());
app.use(express.json());
app.use(morgan('dev'));

app.get('/health', (req, res) => {
    res.status(200).json({ status: 'active' });
});

module.exports = app;
