'use client';

import { useEffect, useState, use } from 'react';
import { api, CareerDetail, Skill } from '@/lib/api';

export default function CareerDetailPage({ params }: { params: Promise<{ slug: string }> }) {
  const resolvedParams = use(params);
  const [career, setCareer] = useState<CareerDetail | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [enrollHours, setEnrollHours] = useState(10);
  const [isEnrolling, setIsEnrolling] = useState(false);
  const [enrollSuccess, setEnrollSuccess] = useState('');

  useEffect(() => {
    async function loadCareer() {
      try {
        const data = await api.getCareerBySlug(resolvedParams.slug);
        setCareer(data);
      } catch (err: any) {
        setError(err.message || 'Failed to load career curriculum.');
      } finally {
        setIsLoading(false);
      }
    }
    loadCareer();
  }, [resolvedParams.slug]);

  const handleEnroll = async () => {
    if (!career) return;
    setIsEnrolling(true);
    setEnrollSuccess('');
    setError('');

    // Check if user is logged in
    const user = await api.getMe();
    if (!user) {
      // Redirect to register with params
      window.location.href = `/register?career=${career.slug}&hours=${enrollHours}`;
      return;
    }

    try {
      await api.enroll(career.id, enrollHours);
      setEnrollSuccess('Enrolled successfully! Redirecting to your dashboard...');
      setTimeout(() => {
        window.location.href = '/dashboard';
      }, 1000);
    } catch (err: any) {
      setError(err.message || 'Enrollment failed.');
      setIsEnrolling(false);
    }
  };

  if (isLoading) {
    return (
      <div className="container" style={{ textAlign: 'center', padding: 'var(--space-16) 0', color: 'var(--text-tertiary)' }}>
        Loading curriculum graph...
      </div>
    );
  }

  if (error || !career) {
    return (
      <div className="container" style={{ textAlign: 'center', padding: 'var(--space-16) 0' }}>
        <h2 style={{ marginBottom: 'var(--space-4)' }}>Career Track Not Found</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: 'var(--space-6)' }}>{error || 'The requested career track does not exist.'}</p>
        <a href="/careers" className="btn btn-secondary">&larr; Back to Careers</a>
      </div>
    );
  }

  // Flatten all skills for quick ID lookup
  const allSkillsMap = new Map<string, Skill>();
  career.competencies.forEach((c) => {
    c.skills.forEach((s) => allSkillsMap.set(s.id, s));
  });

  return (
    <div className="container" style={{ maxWidth: '1000px', paddingTop: 'var(--space-12)', paddingBottom: 'var(--space-16)' }}>
      {/* Header Breadcrumb */}
      <div style={{ marginBottom: 'var(--space-6)' }}>
        <a href="/careers" style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)' }}>
          &larr; Back to all careers
        </a>
      </div>

      {/* Hero Overview */}
      <div className="card" style={{ padding: 'var(--space-8)', marginBottom: 'var(--space-10)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-2)' }}>
          <span style={{ fontSize: 'var(--text-xs)', fontWeight: 700, color: 'var(--color-primary-600)', textTransform: 'uppercase' }}>
            {career.industry_category}
          </span>
          <span className="badge badge-mastered">{career.badge}</span>
        </div>

        <h1 style={{ fontSize: 'var(--text-3xl)', marginBottom: 'var(--space-3)' }}>{career.title}</h1>
        <p style={{ fontSize: 'var(--text-base)', color: 'var(--text-secondary)', lineHeight: 1.7, marginBottom: 'var(--space-6)' }}>
          {career.description}
        </p>

        {/* Enrollment Bar */}
        <div style={{
          backgroundColor: 'var(--bg-surface-subtle)',
          padding: 'var(--space-6)',
          borderRadius: 'var(--radius-md)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: 'var(--space-6)',
        }}>
          <div>
            <span style={{ fontSize: 'var(--text-xs)', fontWeight: 600, color: 'var(--text-tertiary)', textTransform: 'uppercase' }}>
              Your Target Weekly Commitment
            </span>
            <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-4)', marginTop: 'var(--space-1)' }}>
              <input
                type="range"
                min="4"
                max="30"
                step="2"
                value={enrollHours}
                onChange={(e) => setEnrollHours(Number(e.target.value))}
                style={{ width: '160px', cursor: 'pointer' }}
              />
              <strong style={{ fontSize: 'var(--text-base)', color: 'var(--color-primary-600)' }}>
                {enrollHours} hrs/week
              </strong>
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-4)' }}>
            <span style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)' }}>
              Est. ~{Math.ceil(career.avg_months_to_complete * (10 / enrollHours))} months
            </span>
            <button
              onClick={handleEnroll}
              className="btn btn-primary"
              disabled={isEnrolling}
              style={{ minWidth: '180px' }}
            >
              {isEnrolling ? 'Enrolling...' : 'Enroll in this Path ✨'}
            </button>
          </div>
        </div>

        {enrollSuccess && (
          <div style={{ marginTop: 'var(--space-4)', color: 'var(--color-mastery)', fontWeight: 600, fontSize: 'var(--text-sm)' }}>
            {enrollSuccess}
          </div>
        )}
      </div>

      {/* DAG Milestone Tiers (Prerequisite Sequence) */}
      {career.milestones && career.milestones.length > 0 && (
        <section style={{ marginBottom: 'var(--space-12)' }}>
          <h2 style={{ fontSize: 'var(--text-2xl)', marginBottom: 'var(--space-2)' }}>
            Prerequisite Sequence (DAG Tiers)
          </h2>
          <p style={{ color: 'var(--text-secondary)', marginBottom: 'var(--space-6)', fontSize: 'var(--text-sm)' }}>
            Our deterministic graph solver groups skills into unlocked sequence tiers. Tier 1 skills have no prerequisites and unlock on day one. Subsequent tiers unlock automatically as you prove mastery.
          </p>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-6)' }}>
            {career.milestones.map((tier, tierIndex) => (
              <div key={tierIndex} className="card" style={{ backgroundColor: 'var(--bg-canvas)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)', marginBottom: 'var(--space-4)' }}>
                  <span style={{
                    width: '1.75rem',
                    height: '1.75rem',
                    borderRadius: 'var(--radius-full)',
                    backgroundColor: tierIndex === 0 ? 'var(--color-mastery)' : 'var(--color-primary-600)',
                    color: '#ffffff',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: 'var(--text-xs)',
                    fontWeight: 700,
                  }}>
                    {tierIndex + 1}
                  </span>
                  <h3 style={{ fontSize: 'var(--text-lg)', margin: 0 }}>
                    {tierIndex === 0 ? 'Foundation Milestone (Immediate Access)' : `Milestone Level ${tierIndex + 1} (Prerequisite-Gated)`}
                  </h3>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: 'var(--space-4)' }}>
                  {tier.map((skillId) => {
                    const skill = allSkillsMap.get(skillId);
                    if (!skill) return null;
                    return (
                      <div key={skillId} style={{
                        backgroundColor: 'var(--bg-surface)',
                        padding: 'var(--space-4)',
                        borderRadius: 'var(--radius-md)',
                        border: '1px solid var(--border-subtle)',
                      }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-1)' }}>
                          <span className="badge badge-practicing" style={{ fontSize: '0.65rem' }}>
                            {skill.taxonomy}
                          </span>
                          <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-tertiary)' }}>
                            {skill.estimated_hours}h
                          </span>
                        </div>
                        <strong style={{ fontSize: 'var(--text-sm)', display: 'block', color: 'var(--text-primary)' }}>
                          {skill.title}
                        </strong>
                      </div>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Competencies & Free Resources Breakdown */}
      <section>
        <h2 style={{ fontSize: 'var(--text-2xl)', marginBottom: 'var(--space-2)' }}>
          Competency Breakdown &amp; Verified Free Resources
        </h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: 'var(--space-6)', fontSize: 'var(--text-sm)' }}>
          Every topic is paired with 100% legally free documentation, textbooks, and interactive guides.
        </p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-6)' }}>
          {career.competencies.map((comp) => (
            <div key={comp.id} className="card">
              <h3 style={{ fontSize: 'var(--text-xl)', color: 'var(--color-primary-700)', marginBottom: 'var(--space-4)' }}>
                {comp.title}
              </h3>

              <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
                {comp.skills.map((skill) => (
                  <div key={skill.id} style={{
                    padding: 'var(--space-4)',
                    backgroundColor: 'var(--bg-surface-subtle)',
                    borderRadius: 'var(--radius-md)',
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 'var(--space-2)' }}>
                      <div>
                        <strong style={{ fontSize: 'var(--text-base)', color: 'var(--text-primary)' }}>
                          {skill.title}
                        </strong>
                        <p style={{ fontSize: 'var(--text-xs)', color: 'var(--text-secondary)', margin: '0.25rem 0 0 0' }}>
                          {skill.description}
                        </p>
                      </div>
                      <span className="badge badge-mastered" style={{ fontSize: '0.7rem' }}>
                        {skill.taxonomy}
                      </span>
                    </div>

                    {/* Resources */}
                    {skill.topics.map((t) => (
                      <div key={t.id} style={{ marginTop: 'var(--space-3)', paddingTop: 'var(--space-2)', borderTop: '1px solid var(--border-subtle)' }}>
                        <span style={{ fontSize: 'var(--text-xs)', fontWeight: 600, color: 'var(--text-tertiary)' }}>
                          Topic: {t.title}
                        </span>
                        <div style={{ marginTop: 'var(--space-2)', display: 'flex', flexDirection: 'column', gap: 'var(--space-2)' }}>
                          {t.resources.map((r) => (
                            <a
                              key={r.id}
                              href={r.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              style={{
                                display: 'flex',
                                justifyContent: 'space-between',
                                alignItems: 'center',
                                padding: 'var(--space-2) var(--space-3)',
                                backgroundColor: 'var(--bg-surface)',
                                borderRadius: 'var(--radius-sm)',
                                border: '1px solid var(--border-subtle)',
                                fontSize: 'var(--text-xs)',
                                textDecoration: 'none',
                              }}
                            >
                              <span style={{ fontWeight: 600, color: 'var(--text-primary)' }}>
                                🔗 {r.title}
                              </span>
                              <span style={{ color: 'var(--color-primary-600)', fontWeight: 500 }}>
                                {r.provider_name} • {r.estimated_minutes} min
                              </span>
                            </a>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
