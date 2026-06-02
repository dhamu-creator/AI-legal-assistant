// Rate Limiting Middleware
import rateLimit from 'express-rate-limit';

export const chatLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // limit each IP to 100 requests per windowMs
    message: 'Too many chat requests, please try again later.',
});

export const apiLimiter = rateLimit({
    windowMs: 60 * 1000, // 1 minute
    max: 50, // limit each IP to 50 requests per minute
    message: 'Too many API requests, please try again later.',
});

export const authLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 5, // limit each IP to 5 login attempts per 15 minutes
    message: 'Too many login attempts, please try again later.',
});
