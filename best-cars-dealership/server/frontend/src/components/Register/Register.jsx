import React, {useState} from 'react';
import {Link, useNavigate} from 'react-router-dom';
import {api} from '../../api';

export default function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    username: '', first_name: '', last_name: '', email: '', password: ''
  });
  const [error, setError] = useState('');

  function update(event) {
    setForm({...form, [event.target.name]: event.target.value});
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError('');
    try {
      await api('register/', {method: 'POST', body: JSON.stringify(form)});
      navigate('/login');
    } catch (err) {
      setError(err.message);
    }
  }

  return <main>
    <h1>Sign-up</h1>
    <p>Create an account to share your dealership reviews.</p>
    <form onSubmit={handleSubmit}>
      <label htmlFor="username">Username</label>
      <input id="username" name="username" type="text" required
        value={form.username} onChange={update} />

      <label htmlFor="first_name">First Name</label>
      <input id="first_name" name="first_name" type="text" required
        value={form.first_name} onChange={update} />

      <label htmlFor="last_name">Last Name</label>
      <input id="last_name" name="last_name" type="text" required
        value={form.last_name} onChange={update} />

      <label htmlFor="email">Email</label>
      <input id="email" name="email" type="email" required
        value={form.email} onChange={update} />

      <label htmlFor="password">Password</label>
      <input id="password" name="password" type="password" required
        value={form.password} onChange={update} />

      <button type="submit">Register</button>
    </form>
    {error && <p className="error" role="alert">{error}</p>}
    <p>Already registered? <Link to="/login">Login</Link></p>
  </main>;
}
