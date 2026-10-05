'use client';

import { useState, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import { api } from '@/lib/api';

function RegisterForm() {
  const searchParams = useSearchParams();
  const targetCareerSlug = searchParams.get('career');
  const targetHours = Number(searchParams.get('hours')) || 10;

  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setErrorMessage('');

    try {
      await api.register({
        full_name: fullName,
        email: email,
        password: password,
      });

      // If user had a selected career, enroll them immediately!
      if (targetCareerSlug) {
        try {
          const career = await api.getCareerBySlug(targetCareerSlug);
          await api.enroll(career.id, targetHours);
        } catch {
          // If auto-enroll fails, still proceed to dashboard
        }
      }

      window.location.href = '/dashboard';
    } catch (err: any) {
      setErrorMessage(err.message || 'Registration failed.');
      setIsLoading(false);
    }
  };

  return (
    <div className="card" style={{ maxWidth: '440px', margin: '0 auto', padding: 'var(--space-8)' }}>
      <div style={{ textAlign: 'center', marginBottom: 'var(--space-6)' }}>
        <h1 style={{ fontSize: 'var(--text-2xl)', marginBottom: 'var(--space-2)' }}>Create Your Free Account</h1>
        <p style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)' }}>
          {targetCareerSlug ? 'Enroll in your selected career path with personalized pacing.' : 'Begin your journey to demonstrable career readiness.'}
        </p>
      </div>

      {errorMessage && (
        <div style={{
          backgroundColor: '#fef2f2',
          border: '1px solid #fecaca',
          color: '#991b1b',
          padding: 'var(--space-3)',
          borderRadius: 'var(--radius-md)',
          fontSize: 'var(--text-xs)',
          marginBottom: 'var(--space-4)',
        }}>
          {errorMessage}
        </div>
      )}

      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
        <div>
          <label style={{ display: 'block', fontSize: 'var(--text-xs)', fontWeight: 600, marginBottom: 'var(--space-1)' }}>
            Full Name
          </label>
          <input
            type="text"
            required
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            placeholder="e.g. Elena Rostova"
            style={{
              width: '100%',
              padding: 'var(--space-3)',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-default)',
              fontSize: 'var(--text-sm)',
              boxSizing: 'border-box',
            }}
          />
        </div>

        <div>
          <label style={{ display: 'block', fontSize: 'var(--text-xs)', fontWeight: 600, marginBottom: 'var(--space-1)' }}>
            Email Address
          </label>
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            style={{
              width: '100%',
              padding: 'var(--space-3)',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-default)',
              fontSize: 'var(--text-sm)',
              boxSizing: 'border-box',
            }}
          />
        </div>

        <div>
          <label style={{ display: 'block', fontSize: 'var(--text-xs)', fontWeight: 600, marginBottom: 'var(--space-1)' }}>
            Password (min 8 characters)
          </label>
          <input
            type="password"
            required
            minLength={8}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
            style={{
              width: '100%',
              padding: 'var(--space-3)',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-default)',
              fontSize: 'var(--text-sm)',
              boxSizing: 'border-box',
            }}
          />
        </div>

        <button
          type="submit"
          className="btn btn-primary"
          disabled={isLoading}
          style={{ width: '100%', marginTop: 'var(--space-2)' }}
        >
          {isLoading ? 'Creating Account...' : 'Get Started Free ✨'}
        </button>
      </form>

      <div style={{ textAlign: 'center', marginTop: 'var(--space-6)', fontSize: 'var(--text-xs)', color: 'var(--text-secondary)' }}>
        Already have an account?{' '}
        <a href="/login" style={{ fontWeight: 600, color: 'var(--color-primary-600)' }}>
          Sign In
        </a>
      </div>
    </div>
  );
}

export default function RegisterPage() {
  return (
    <div className="container" style={{ paddingTop: 'var(--space-16)', paddingBottom: 'var(--space-16)' }}>
      <Suspense fallback={<div style={{ textAlign: 'center' }}>Loading form...</div>}>
        <RegisterForm />
      </Suspense>
    </div>
  );
}
