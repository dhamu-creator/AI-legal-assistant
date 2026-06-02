import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

export default function Auth() {
    const { login, register, logout, user } = useAuth();
    const [mode, setMode] = useState('login');
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (mode === 'login') {
            await login(email, password);
            alert('Logged in');
        } else {
            await register(name, email, password);
            alert('Registered and logged in');
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
            <div className="w-full max-w-md bg-white p-8 rounded shadow">
                <h2 className="text-2xl font-bold mb-4">{mode === 'login' ? 'Login' : 'Register'}</h2>
                {user && (
                    <div className="mb-4 p-3 bg-green-50">Logged in as: {user.name}</div>
                )}
                <form onSubmit={handleSubmit} className="space-y-4">
                    {mode === 'register' && (
                        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Full name" className="w-full px-3 py-2 border rounded" />
                    )}
                    <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" className="w-full px-3 py-2 border rounded" />
                    <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" className="w-full px-3 py-2 border rounded" />
                    <div className="flex gap-2">
                        <button type="submit" className="px-4 py-2 bg-indigo-600 text-white rounded">{mode === 'login' ? 'Login' : 'Register'}</button>
                        <button type="button" onClick={() => setMode(mode === 'login' ? 'register' : 'login')} className="px-4 py-2 border rounded">
                            {mode === 'login' ? 'Switch to register' : 'Switch to login'}
                        </button>
                        <button type="button" onClick={logout} className="px-4 py-2 border rounded">Logout</button>
                    </div>
                </form>
            </div>
        </div>
    );
}
