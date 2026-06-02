// Centralized Error Handling Middleware
const errorHandler = (err, req, res, next) => {
    console.error(err.stack);

    // MongoDB Validation Errors
    if (err.name === 'ValidationError') {
        return res.status(400).json({
            success: false,
            message: 'Validation Error',
            errors: Object.values(err.errors).map((e) => e.message),
        });
    }

    // MongoDB Duplicate Key Error
    if (err.code === 11000) {
        return res.status(400).json({
            success: false,
            message: 'Duplicate Field Error',
            field: Object.keys(err.keyPattern)[0],
        });
    }

    // JWT Errors
    if (err.name === 'JsonWebTokenError') {
        return res.status(401).json({
            success: false,
            message: 'Invalid Token',
        });
    }

    if (err.name === 'TokenExpiredError') {
        return res.status(401).json({
            success: false,
            message: 'Token Expired',
        });
    }

    // Default Error
    res.status(err.status || 500).json({
        success: false,
        message: err.message || 'Internal Server Error',
    });
};

export default errorHandler;
