import dotenv from 'dotenv';
import jwt from 'jsonwebtoken';
import User from '../models/User.js';

dotenv.config();

const signToken = (user) => {
  const payload = { id: user._id, email: user.email };
  const secret = process.env.JWT_SECRET || 'change_this_secret';
  const expiresIn = process.env.JWT_EXPIRES_IN || '1h';
  return jwt.sign(payload, secret, { expiresIn });
};

class AuthController {
  async register(req, res, next) {
    try {
      const { name, email, password, language } = req.body;
      if (!name || !email || !password) {
        return res.status(400).json({ success: false, message: 'Name, email and password are required' });
      }

      const existing = await User.findOne({ email });
      if (existing) {
        return res.status(409).json({ success: false, message: 'Email already registered' });
      }

      const user = new User({ name, email, password, language });
      await user.save();

      const token = signToken(user);
      res.status(201).json({ success: true, data: { user: { id: user._id, name: user.name, email: user.email }, token } });
    } catch (err) {
      next(err);
    }
  }

  async login(req, res, next) {
    try {
      const { email, password } = req.body;
      if (!email || !password) {
        return res.status(400).json({ success: false, message: 'Email and password required' });
      }

      const user = await User.findOne({ email });
      if (!user) return res.status(401).json({ success: false, message: 'Invalid credentials' });

      const match = await user.comparePassword(password);
      if (!match) return res.status(401).json({ success: false, message: 'Invalid credentials' });

      const token = signToken(user);
      res.status(200).json({ success: true, data: { user: { id: user._id, name: user.name, email: user.email }, token } });
    } catch (err) {
      next(err);
    }
  }

  async me(req, res, next) {
    try {
      const user = await User.findById(req.user.id).select('-password');
      if (!user) return res.status(404).json({ success: false, message: 'User not found' });
      res.status(200).json({ success: true, data: user });
    } catch (err) {
      next(err);
    }
  }
}

export default new AuthController();
