'use client';

import { useState } from 'react';
import { api, DiscoveryRecommendation } from '@/lib/api';

export default function DiscoverPage() {
  const [step, setStep] = useState(1);
  const [workStyle, setWorkStyle] = useState('ANALYTICAL');
  const [hoursPerWeek, setHoursPerWeek] = useState(10);
  const [environment, setEnvironment] = useState('REMOTE');
  const [isLoading, setIsLoading] = useState(false);
  const [recommendations, setRecommendations] = useState<DiscoveryRecommendation[] | null>(null);
  const [errorMessage, setErrorMessage] = useState('');

  const workStyles = [
    { id: 'ANALYTICAL', title: 'Analytical & Problem-Solving', desc: 'Working with logical systems, math, code, or data structures.' },
    { id: 'HANDS_ON', title: 'Tactile & Practical Execution', desc: 'Working with physical tools, circuits, equipment, or building things.' },
    { id: 'DETAIL_ORIENTED', title: 'Meticulous & Structured Records', desc: 'Working with compliance, medical terminology, audit trails, and rules.' },
  ];

  const environments = [
    { id: 'REMOTE', title: 'Digital / Remote Desk', desc: 'Working primarily on a computer from anywhere.' },
    { id: 'CLINICAL', title: 'Healthcare & Clinical Services', desc: 'Hospital, clinic, or medical administrative environment.' },
    { id: 'FIELD', title: 'Workshops, Job Sites & Field Work', desc: 'On-site installation, maintenance, and physical environments.' },
  ];

  const handleEvaluate = async () => {
    setIsLoading(true);
    setErrorMessage('');
    try {
      const res = await api.evaluateDiscovery({
        interests: [],
        available_hours_per_week: hoursPerWeek,
        work_style: workStyle,
        environment: environment,
      });
      setRecommendations(res.recommendations);
    } catch (err: any) {
      setErrorMessage(err.message || 'Failed to calculate recommendations. Is the backend server running?');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container" style={{ maxWidth: '800px', paddingTop: 'var(--space-12)', paddingBottom: 'var(--space-16)' }}>
      {/* Header */}
      <div style={{ textAlign: 'center', marginBottom: 'var(--space-10)' }}>
        <span style={{
          fontSize: 'var(--text-xs)',
          fontWeight: 700,
          color: 'var(--color-primary-600)',
          textTransform: 'uppercase',
          letterSpacing: '0.05em',
        }}>
          Career Discovery Engine
        </span>
        <h1 style={{ fontSize: 'var(--text-3xl)', marginTop: 'var(--space-2)', marginBottom: 'var(--space-3)' }}>
          Discover Your Ideal Career Direction
        </h1>
        <p style={{ color: 'var(--text-secondary)', maxWidth: '580px', margin: '0 auto' }}>
          Answer 3 quick questions about your natural working style and available hours. We will match you against verified career pathways.
        </p>
      </div>

      {errorMessage && (
        <div style={{
          backgroundColor: '#fef2f2',
          border: '1px solid #fecaca',
          color: '#991b1b',
          padding: 'var(--space-4)',
          borderRadius: 'var(--radius-md)',
          marginBottom: 'var(--space-6)',
          fontSize: 'var(--text-sm)',
        }}>
          {errorMessage}
        </div>
      )}

      {/* Results View */}
      {recommendations ? (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-8)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h2>Your Top Matched Career Tracks</h2>
            <button
              onClick={() => setRecommendations(null)}
              className="btn btn-secondary"
              style={{ fontSize: 'var(--text-xs)' }}
            >
              &larr; Retake Quiz
            </button>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-6)' }}>
            {recommendations.map((rec, index) => (
              <div key={rec.career_id} className="card" style={{
                borderLeft: index === 0 ? '4px solid var(--color-primary-600)' : '1px solid var(--border-subtle)',
                position: 'relative',
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 'var(--space-3)' }}>
                  <div>
                    <span style={{ fontSize: 'var(--text-xs)', fontWeight: 700, color: 'var(--color-primary-600)', textTransform: 'uppercase' }}>
                      {rec.category}
                    </span>
                    <h3 style={{ fontSize: 'var(--text-xl)', marginTop: 'var(--space-1)' }}>{rec.title}</h3>
                  </div>

                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: 'var(--space-2)',
                    backgroundColor: 'var(--color-mastery-light)',
                    color: 'var(--color-mastery)',
                    padding: 'var(--space-1) var(--space-4)',
                    borderRadius: 'var(--radius-full)',
                    fontWeight: 700,
                    fontSize: 'var(--text-sm)',
                  }}>
                    <span>{rec.match_percentage}% Match</span>
                  </div>
                </div>

                <div style={{
                  backgroundColor: 'var(--bg-surface-subtle)',
                  padding: 'var(--space-4)',
                  borderRadius: 'var(--radius-md)',
                  marginTop: 'var(--space-4)',
                  marginBottom: 'var(--space-4)',
                }}>
                  <p style={{ margin: 0, fontSize: 'var(--text-sm)', color: 'var(--text-primary)', lineHeight: 1.6 }}>
                    <strong>Why this fits:</strong> {rec.rationale}
                  </p>
                </div>

                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  flexWrap: 'wrap',
                  gap: 'var(--space-4)',
                  borderTop: '1px solid var(--border-subtle)',
                  paddingTop: 'var(--space-4)',
                }}>
                  <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-tertiary)' }}>
                    Est. {rec.estimated_months} months at {hoursPerWeek} hrs/week
                  </span>

                  <div style={{ display: 'flex', gap: 'var(--space-3)' }}>
                    <a
                      href={`/careers/${rec.slug}`}
                      className="btn btn-secondary"
                      style={{ fontSize: 'var(--text-sm)', padding: 'var(--space-2) var(--space-4)' }}
                    >
                      View Curriculum &rarr;
                    </a>
                    <a
                      href={`/register?career=${rec.slug}&hours=${hoursPerWeek}`}
                      className="btn btn-primary"
                      style={{ fontSize: 'var(--text-sm)', padding: 'var(--space-2) var(--space-4)' }}
                    >
                      Enroll in Path
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : (
        /* Multi-step Quiz */
        <div className="card" style={{ padding: 'var(--space-8)' }}>
          {/* Step 1: Work Style */}
          {step === 1 && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-6)' }}>
              <div>
                <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-tertiary)' }}>Step 1 of 3</span>
                <h3 style={{ fontSize: 'var(--text-xl)', marginTop: 'var(--space-1)' }}>
                  How do you naturally prefer to solve problems?
                </h3>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)' }}>
                {workStyles.map((item) => (
                  <label
                    key={item.id}
                    onClick={() => setWorkStyle(item.id)}
                    style={{
                      display: 'flex',
                      alignItems: 'flex-start',
                      gap: 'var(--space-4)',
                      padding: 'var(--space-4)',
                      borderRadius: 'var(--radius-md)',
                      border: workStyle === item.id ? '2px solid var(--color-primary-600)' : '1px solid var(--border-default)',
                      backgroundColor: workStyle === item.id ? 'var(--color-primary-50)' : 'var(--bg-surface)',
                      cursor: 'pointer',
                      transition: 'all var(--transition-fast)',
                    }}
                  >
                    <input
                      type="radio"
                      name="workStyle"
                      checked={workStyle === item.id}
                      onChange={() => setWorkStyle(item.id)}
                      style={{ marginTop: '0.25rem' }}
                    />
                    <div>
                      <strong style={{ display: 'block', color: 'var(--text-primary)' }}>{item.title}</strong>
                      <span style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)' }}>{item.desc}</span>
                    </div>
                  </label>
                ))}
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: 'var(--space-4)' }}>
                <button onClick={() => setStep(2)} className="btn btn-primary">
                  Next: Time Commitment &rarr;
                </button>
              </div>
            </div>
          )}

          {/* Step 2: Hours Per Week */}
          {step === 2 && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-6)' }}>
              <div>
                <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-tertiary)' }}>Step 2 of 3</span>
                <h3 style={{ fontSize: 'var(--text-xl)', marginTop: 'var(--space-1)' }}>
                  How many hours per week can you realistically dedicate?
                </h3>
                <p style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)', marginTop: 'var(--space-1)' }}>
                  Veyra uses this to dynamically configure your milestone pacing and projected completion timeline.
                </p>
              </div>

              <div style={{ padding: 'var(--space-4) 0' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 'var(--space-2)' }}>
                  <span style={{ fontWeight: 700, fontSize: 'var(--text-lg)', color: 'var(--color-primary-600)' }}>
                    {hoursPerWeek} hours / week
                  </span>
                  <span style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)' }}>
                    {hoursPerWeek <= 6 ? 'Steady micro-pacing' : hoursPerWeek <= 14 ? 'Standard part-time pace' : 'Accelerated intensive pace'}
                  </span>
                </div>
                <input
                  type="range"
                  min="2"
                  max="40"
                  step="2"
                  value={hoursPerWeek}
                  onChange={(e) => setHoursPerWeek(Number(e.target.value))}
                  style={{ width: '100%', height: '8px', cursor: 'pointer' }}
                />
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 'var(--space-4)' }}>
                <button onClick={() => setStep(1)} className="btn btn-secondary">
                  &larr; Back
                </button>
                <button onClick={() => setStep(3)} className="btn btn-primary">
                  Next: Work Environment &rarr;
                </button>
              </div>
            </div>
          )}

          {/* Step 3: Work Environment */}
          {step === 3 && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-6)' }}>
              <div>
                <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-tertiary)' }}>Step 3 of 3</span>
                <h3 style={{ fontSize: 'var(--text-xl)', marginTop: 'var(--space-1)' }}>
                  What work environment feels most energizing to you?
                </h3>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)' }}>
                {environments.map((item) => (
                  <label
                    key={item.id}
                    onClick={() => setEnvironment(item.id)}
                    style={{
                      display: 'flex',
                      alignItems: 'flex-start',
                      gap: 'var(--space-4)',
                      padding: 'var(--space-4)',
                      borderRadius: 'var(--radius-md)',
                      border: environment === item.id ? '2px solid var(--color-primary-600)' : '1px solid var(--border-default)',
                      backgroundColor: environment === item.id ? 'var(--color-primary-50)' : 'var(--bg-surface)',
                      cursor: 'pointer',
                      transition: 'all var(--transition-fast)',
                    }}
                  >
                    <input
                      type="radio"
                      name="environment"
                      checked={environment === item.id}
                      onChange={() => setEnvironment(item.id)}
                      style={{ marginTop: '0.25rem' }}
                    />
                    <div>
                      <strong style={{ display: 'block', color: 'var(--text-primary)' }}>{item.title}</strong>
                      <span style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)' }}>{item.desc}</span>
                    </div>
                  </label>
                ))}
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 'var(--space-4)' }}>
                <button onClick={() => setStep(2)} className="btn btn-secondary" disabled={isLoading}>
                  &larr; Back
                </button>
                <button
                  onClick={handleEvaluate}
                  className="btn btn-primary"
                  disabled={isLoading}
                  style={{ minWidth: '180px' }}
                >
                  {isLoading ? 'Calculating Matches...' : 'Find My Career Match ✨'}
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
