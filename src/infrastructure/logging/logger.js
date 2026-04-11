// src/infrastructure/logging/logger.js
const winston = require('winston');

const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        // ফাইল লগার (সব লগ এখানে থাকবে)
        new winston.transports.File({ filename: 'logs/combined.log' }),
        // এরর লগার (শুধু বিপদগুলো এখানে থাকবে)
        new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
    ],
});

// যদি ডেভেলপমেন্ট মোডে থাকে তবে কনসোলেও দেখাবে
if (process.env.NODE_ENV !== 'production') {
    logger.add(new winston.transports.Console({
        format: winston.format.simple(),
    }));
}

module.exports = logger;
