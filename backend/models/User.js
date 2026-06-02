import mongoose from 'mongoose';
import bcrypt from 'bcryptjs';

const userSchema = new mongoose.Schema(
    {
        name: {
            type: String,
            required: true,
            trim: true,
        },
        email: {
            type: String,
            required: true,
            unique: true,
            lowercase: true,
            trim: true,
        },
        password: {
            type: String,
            required: true,
        },
        phone: {
            type: String,
            trim: true,
        },
        language: {
            type: String,
            enum: ['en', 'ta', 'hi', 'te', 'ml', 'ka'],
            default: 'en',
        },
        savedReports: [
            {
                type: mongoose.Schema.Types.ObjectId,
                ref: 'FIRReport',
            },
        ],
        chatSessions: [
            {
                type: mongoose.Schema.Types.ObjectId,
                ref: 'ChatSession',
            },
        ],
        preferences: {
            darkMode: { type: Boolean, default: false },
            notifications: { type: Boolean, default: true },
        },
    },
    { timestamps: true }
);

// Hash password before saving
userSchema.pre('save', async function () {
    if (!this.isModified('password')) return;
    const salt = await bcrypt.genSalt(10);
    this.password = await bcrypt.hash(this.password, salt);
});

// Compare plaintext password with hashed
userSchema.methods.comparePassword = async function (candidatePassword) {
    return bcrypt.compare(candidatePassword, this.password);
};

const User = mongoose.model('User', userSchema);
export default User;
