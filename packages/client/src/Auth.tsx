import { useState } from 'react';
import { trpc } from './trpc';

export function Auth() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');

  const signup = trpc.auth.signup.useMutation();
  const login = trpc.auth.login.useMutation();

  const handleSignup = () => {
    signup.mutate({ email, password, name });
  };

  const handleLogin = () => {
    login.mutate({ email, password });
  };

  return (
    <div className="flex flex-col gap-4">
      <input
        type="text"
        placeholder="Name (optional)"
        value={name}
        onChange={(e) => setName(e.target.value)}
        className="p-2 bg-gray-800 rounded"
      />
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="p-2 bg-gray-800 rounded"
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="p-2 bg-gray-800 rounded"
      />
      <div className="flex gap-4">
        <button onClick={handleSignup} className="p-2 bg-blue-500 rounded">
          Sign Up
        </button>
        <button onClick={handleLogin} className="p-2 bg-green-500 rounded">
          Login
        </button>
      </div>
      {signup.error && <p className="text-red-500">{signup.error.message}</p>}
      {login.error && <p className="text-red-500">{login.error.message}</p>}
      {login.data && <p className="text-green-500">Logged in successfully! Token: {login.data.token}</p>}
    </div>
  );
}
