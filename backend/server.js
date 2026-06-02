import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import dotenv from 'dotenv';
import mongoose from 'mongoose';
import errorHandler from './middleware/errorHandler.js';
import chatRoutes from './routes/chatRoutes.js';
import firRoutes from './routes/firRoutes.js';
import legalRoutes from './routes/legalRoutes.js';
import authRoutes from './routes/authRoutes.js';

dotenv.config();

const app = express();

// ==================== MIDDLEWARE ====================
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ limit: '50mb', extended: true }));
app.use(cors());
app.use(helmet());
app.use(morgan('dev'));

// ==================== DATABASE CONNECTION ====================
const connectDB = async () => {
    try {
        const conn = await mongoose.connect(process.env.MONGO_URI || 'mongodb://localhost:27017/ai-legal-assistant');
        console.log(`✅ MongoDB Connected: ${conn.connection.host}`);
    } catch (error) {
        console.error(`❌ Error connecting to MongoDB: ${error.message}`);
        process.exit(1);
    }
};

// Start server only after DB connection to avoid Mongoose buffering/timeouts
const start = async () => {
    await connectDB();

    // Health check
    app.get('/api/health', (req, res) => {
        res.status(200).json({
            status: 'ok',
            message: 'AI Legal Assistant API is running',
            timestamp: new Date().toISOString(),
        });
    });

    // Ready check (includes DB state)
    app.get('/api/ready', (req, res) => {
        const ready = mongoose.connection && mongoose.connection.readyState === 1;
        res.status(200).json({ ready, state: mongoose.connection ? mongoose.connection.readyState : 0 });
    });

    // API Routes
    app.use('/api/chat', chatRoutes);
    app.use('/api/fir', firRoutes);
    app.use('/api/legal', legalRoutes);
    app.use('/api/auth', authRoutes);

    // 404 and error handlers
    app.use((req, res) => {
        res.status(404).json({ success: false, message: 'Route not found' });
    });
    app.use(errorHandler);

    const PORT = process.env.PORT || 5000;
    const server = app.listen(PORT, () => {
        console.log(`\n╔═══════════════════════════════════════════════════════╗\n║   🏛️  AI LEGAL ASSISTANT - Backend Server              ║\n║   Status: 🟢 Running                                   ║\n║   Port: ${PORT}                                              ║\n║   Environment: ${process.env.NODE_ENV || 'development'}                          ║\n║   Database: MongoDB Connected                         ║\n╚═══════════════════════════════════════════════════════╝\n    `);
    });

    process.on('SIGTERM', () => {
        console.log('SIGTERM signal received: closing HTTP server');
        server.close(() => {
            console.log('HTTP server closed');
            mongoose.connection.close(false, () => {
                console.log('MongoDB connection closed');
                process.exit(0);
            });
        });
    });
};

start().catch((err) => {
    console.error('Failed to start server:', err);
    process.exit(1);
});

export default app;
