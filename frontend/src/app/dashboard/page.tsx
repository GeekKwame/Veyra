'use client';

import { useEffect, useState } from 'react';
import { api, UserRoadmap, User } from '@/lib/api';

export default function DashboardPage() {
  const [roadmap, setRoadmap] = useState<UserRoadmap | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [hoursCommitment, setHoursCommitment] = useState(10);
  const [isRecalibrating, setIsRecalibrating] = useState(false);
  const [recalibrateNotice, setRecalibrateNotice] = useState('');

  useEffect(() => {
    async function loadDashboard() {
      try {
        const currentUser = await api.getMe();
        if (!currentUser) {
          window.location.href = '/login';
          return;
        }
        setUser(currentUser);

        const activeRoadmap = await api.getActiveRoadmap();
        setRoadmap(activeRoadmap);
        setHoursCommitment(activeRoadmap.committed_hours_per_week);
      } catch (err: any) {
        if (err.message && err.message.includes('No active roadmap')) {
          setRoadmap(null);
        } else {
          setError(err.message || 'Failed to load active roadmap.');
        }
      } finally {
        setIsLoading(false);
      }
    }
    loadDashboard();
  }, []);

  const handleRecalibrate = async () => {
    if (!roadmap) return;
    setIsRecalibrating(true);
    setRecalibrateNotice('');

    try {
      const res = await api.recalibratePacing(hoursCommitment);
      setRoadmap((prev) => prev ? {
        ...prev,
        committed_hours_per_week: res.committed_hours_per_week,
        projected_completion_date: res.projected_completion_date,
      } : null);
      setRecalibrateNotice(`Schedule successfully recalibrated for ${hoursCommitment} hrs/week.`);
    } catch (err: any) {
      setError(err.message || 'Recalibration failed.');
    } finally {
      setIsRecalibrating(false);
    }
  };

  const handleLogout = async () => {
    await api.logout();
    window.location.href = '/';
  };

  if (isLoading) {
    return (
      <div className="container" style={{ textAlign: 'center', padding: 'var(--space-16) 0', color: 'var(--text-tertiary)' }}>
        Loading your career roadmap...
      </div>
    );
  }

  // If no roadmap enrolled yet
  if (!roadmap) {
    return (
      <div className="container" style={{ maxWidth: '680px', paddingTop: 'var(--space-16)', textAlign: 'center' }}>
        <div className="card" style={{ padding: 'var(--space-10)' }}>
          <h1 style={{ fontSize: 'var(--text-2xl)', marginBottom: 'var(--space-3)' }}>
            Welcome, {user?.full_name || 'Learner'}! 👋
          </h1>
          <p style={{ color: 'var(--text-secondary)', marginBottom: 'var(--space-6)', lineHeight: 1.6 }}>
            You haven&apos;t enrolled in an active career path yet. Take our 2-minute discovery questionnaire or explore the catalog to begin.
          </p>
          <div style={{ display: 'flex', gap: 'var(--space-4)', justifyContent: 'center' }}>
            <a href="/discover" className="btn btn-primary">Take Career Discovery Quiz &rarr;</a>
            <a href="/careers" className="btn btn-secondary">Browse Career Catalog</a>
          </div>
        </div>
      </div>
    );
  }

  // Find next action skill (first AVAILABLE or IN_PROGRESS)
  const nextSkill = roadmap.skill_progresses.find((p) => p.status === 'IN_PROGRESS' || p.status === 'AVAILABLE');

  return (
    <div className="container" style={{ maxWidth: '1000px', paddingTop: 'var(--space-10)', paddingBottom: 'var(--space-16)' }}>
      {/* Top Banner */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-6)', flexWrap: 'wrap', gap: 'var(--space-4)' }}>
        <div>
          <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-tertiary)' }}>Active Career Track</span>
          <h1 style={{ fontSize: 'var(--text-2xl)', marginTop: '0.25rem' }}>{roadmap.career_title}</h1>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-4)' }}>
          <div style={{
            backgroundColor: 'var(--color-primary-50)',
            color: 'var(--color-primary-800)',
            padding: 'var(--space-2) var(--space-4)',
            borderRadius: 'var(--radius-md)',
            fontWeight: 700,
            fontSize: 'var(--text-sm)',
          }}>
            Readiness Index: {roadmap.readiness_score}%
          </div>
          <button onClick={handleLogout} className="btn btn-secondary" style={{ fontSize: 'var(--text-xs)' }}>
            Sign Out
          </button>
        </div>
      </div>

      {error && (
        <div style={{
          backgroundColor: '#fef2f2',
          border: '1px solid #fecaca',
          color: '#991b1b',
          padding: 'var(--space-3)',
          borderRadius: 'var(--radius-md)',
          marginBottom: 'var(--space-6)',
          fontSize: 'var(--text-sm)',
        }}>
          {error}
        </div>
      )}

      {/* Primary Metrics Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
        gap: 'var(--space-4)',
        marginBottom: 'var(--space-8)',
      }}>
        <div className="card" style={{ padding: 'var(--space-5)' }}>
          <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-tertiary)' }}>Mastery Progress</span>
          <div style={{ fontSize: 'var(--text-2xl)', fontWeight: 800, color: 'var(--color-mastery)', marginTop: 'var(--space-1)' }}>
            {roadmap.progress_summary.completion_pct}%
          </div>
          <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-secondary)' }}>
            {roadmap.progress_summary.mastered} of {roadmap.progress_summary.total} skills verified
          </span>
        </div>

        <div className="card" style={{ padding: 'var(--space-5)' }}>
          <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-tertiary)' }}>Target Completion</span>
          <div style={{ fontSize: 'var(--text-xl)', fontWeight: 700, color: 'var(--text-primary)', marginTop: 'var(--space-1)' }}>
            {roadmap.projected_completion_date ? new Date(roadmap.projected_completion_date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : 'Calculating...'}
          </div>
          <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-secondary)' }}>
            At {roadmap.committed_hours_per_week} hours per week
          </span>
        </div>

        <div className="card" style={{ padding: 'var(--space-5)' }}>
          <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-tertiary)' }}>Skills Unlocked</span>
          <div style={{ fontSize: 'var(--text-2xl)', fontWeight: 800, color: 'var(--color-primary-600)', marginTop: 'var(--space-1)' }}>
            {roadmap.progress_summary.available + roadmap.progress_summary.in_progress} Ready
          </div>
          <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-secondary)' }}>
            {roadmap.progress_summary.locked} prerequisite-locked
          </span>
        </div>
      </div>

      {/* Next Action Focus Card */}
      {nextSkill && (
        <div className="card" style={{
          padding: 'var(--space-6)',
          backgroundColor: 'linear-gradient(135deg, var(--bg-surface), var(--color-primary-50))',
          borderLeft: '4px solid var(--color-primary-600)',
          marginBottom: 'var(--space-8)',
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 'var(--space-4)' }}>
            <div>
              <span style={{ fontSize: 'var(--text-xs)', fontWeight: 700, color: 'var(--color-primary-600)', textTransform: 'uppercase' }}>
                Your Next Objective
              </span>
              <h2 style={{ fontSize: 'var(--text-xl)', marginTop: '0.25rem' }}>{nextSkill.skill.title}</h2>
              <p style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)', margin: '0.25rem 0 0 0' }}>
                {nextSkill.skill.description}
              </p>
            </div>

            <a
              href={`/careers/${roadmap.career_slug}`}
              className="btn btn-primary"
              style={{ padding: 'var(--space-3) var(--space-6)' }}
            >
              Start Skill Practice &rarr;
            </a>
          </div>
        </div>
      )}

      {/* Dynamic Pacing Recalibration Tool */}
      <div className="card" style={{ padding: 'var(--space-6)', marginBottom: 'var(--space-8)', backgroundColor: 'var(--bg-surface-subtle)' }}>
        <h3 style={{ fontSize: 'var(--text-base)', marginBottom: 'var(--space-2)' }}>
          Adaptive Pacing Recalibration
        </h3>
        <p style={{ fontSize: 'var(--text-xs)', color: 'var(--text-secondary)', marginBottom: 'var(--space-4)' }}>
          Life gets busy or your schedule opens up. Adjust your weekly hours below — our pacing solver recalculates your roadmap target dates in real time without resetting mastered skills.
        </p>

        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-6)', flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-4)' }}>
            <input
              type="range"
              min="2"
              max="40"
              step="2"
              value={hoursCommitment}
              onChange={(e) => setHoursCommitment(Number(e.target.value))}
              style={{ width: '180px', cursor: 'pointer' }}
            />
            <strong style={{ fontSize: 'var(--text-sm)', color: 'var(--color-primary-600)' }}>
              {hoursCommitment} hrs / week
            </strong>
          </div>

          <button
            onClick={handleRecalibrate}
            className="btn btn-secondary"
            disabled={isRecalibrating || hoursCommitment === roadmap.committed_hours_per_week}
            style={{ fontSize: 'var(--text-xs)' }}
          >
            {isRecalibrating ? 'Recalibrating...' : 'Recalibrate Timeline'}
          </button>
        </div>

        {recalibrateNotice && (
          <div style={{ marginTop: 'var(--space-3)', color: 'var(--color-mastery)', fontSize: 'var(--text-xs)', fontWeight: 600 }}>
            {recalibrateNotice}
          </div>
        )}
      </div>

      {/* Sequential Skills Roadmap List */}
      <div>
        <h3 style={{ fontSize: 'var(--text-xl)', marginBottom: 'var(--space-4)' }}>Curriculum Roadmap &amp; Milestone States</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)' }}>
          {roadmap.skill_progresses.map((p) => {
            const isMastered = p.status === 'MASTERED';
            const isAvailable = p.status === 'AVAILABLE';
            const isInProgress = p.status === 'IN_PROGRESS' || p.status === 'PRACTICING';
            const isLocked = p.status === 'LOCKED';

            return (
              <div
                key={p.id}
                className="card"
                style={{
                  padding: 'var(--space-4)',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  opacity: isLocked ? 0.7 : 1,
                  backgroundColor: isMastered ? 'var(--color-mastery-light)' : 'var(--bg-surface)',
                  borderLeft: isMastered
                    ? '4px solid var(--color-mastery)'
                    : isAvailable || isInProgress
                    ? '4px solid var(--color-primary-600)'
                    : '4px solid var(--border-default)',
                }}
              >
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-2)' }}>
                    <strong style={{ fontSize: 'var(--text-sm)', color: 'var(--text-primary)' }}>
                      {p.skill.title}
                    </strong>
                    <span className="badge badge-practicing" style={{ fontSize: '0.65rem' }}>
                      {p.skill.taxonomy}
                    </span>
                  </div>
                  <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-secondary)' }}>
                    Est. {p.skill.estimated_hours}h • {p.skill.topics.length} verified topics
                  </span>
                </div>

                <div>
                  {isMastered && (
                    <span className="badge badge-mastered">
                      ✓ Mastered ({p.score_percentage}%)
                    </span>
                  )}
                  {isInProgress && (
                    <span className="badge badge-practicing">
                      ● In Progress
                    </span>
                  )}
                  {isAvailable && (
                    <span className="badge badge-practicing" style={{ backgroundColor: 'var(--color-primary-100)', color: 'var(--color-primary-700)' }}>
                      Unlocked &amp; Ready
                    </span>
                  )}
                  {isLocked && (
                    <span className="badge badge-locked">
                      🔒 Prerequisite Locked
                    </span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
