export default function HomePage() {
  const seedCareers = [
    {
      category: 'Healthcare',
      title: 'Medical Billing & Coding',
      description: 'Master ICD-10, CPT, and healthcare compliance with verified simulations and practice claims.',
      duration: '4-6 months',
      badge: 'High Demand',
    },
    {
      category: 'Finance',
      title: 'Staff Bookkeeper & Junior Accountant',
      description: 'Master double-entry bookkeeping, GAAP principles, reconciliations, and financial reporting.',
      duration: '5-7 months',
      badge: 'Essential',
    },
    {
      category: 'Skilled Trades',
      title: 'Residential Electrician Foundations',
      description: 'Understand Ohm’s Law, NEC safety standards, circuitry diagrams, and apprentice prep drills.',
      duration: '6-9 months',
      badge: 'Hands-on',
    },
    {
      category: 'Technology',
      title: 'Junior Fullstack Web Developer',
      description: 'Build production APIs, modern reactive user interfaces, and relational database schemas.',
      duration: '6-8 months',
      badge: 'Project-heavy',
    },
  ];

  const loopSteps = [
    { step: '01', title: 'Discover', desc: 'Find career paths tailored to your strengths, available hours, and constraints.' },
    { step: '02', title: 'Learn', desc: 'Study only verified, 100% legally free courses, videos, and documentation.' },
    { step: '03', title: 'Practice', desc: 'Solve hands-on drills and situational scenarios instead of just watching videos.' },
    { step: '04', title: 'Build', desc: 'Produce authentic capstone projects evaluated against rigorous industry rubrics.' },
    { step: '05', title: 'Assess', desc: 'Test your understanding with timed situational evaluations and diagnostics.' },
    { step: '06', title: 'Prove', desc: 'Build a verifiable portfolio showcasing exactly what you can actually do.' },
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-16)' }}>
      {/* Hero Section */}
      <section style={{
        paddingTop: 'var(--space-16)',
        paddingBottom: 'var(--space-12)',
        background: 'radial-gradient(ellipse at 50% 0%, rgba(124, 58, 237, 0.08) 0%, transparent 70%)',
        textAlign: 'center',
      }}>
        <div className="container" style={{ maxWidth: '840px' }}>
          <div style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: 'var(--space-2)',
            padding: 'var(--space-1) var(--space-4)',
            backgroundColor: 'var(--color-primary-50)',
            color: 'var(--color-primary-700)',
            borderRadius: 'var(--radius-full)',
            fontSize: 'var(--text-xs)',
            fontWeight: 700,
            textTransform: 'uppercase',
            letterSpacing: '0.05em',
            marginBottom: 'var(--space-6)',
          }}>
            100% Free • Career-Agnostic • Built on Proven Mastery
          </div>

          <h1 style={{ marginBottom: 'var(--space-6)' }}>
            Stop collecting course certificates.<br />
            <span style={{
              background: 'linear-gradient(135deg, var(--color-primary-600), var(--color-accent-600))',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}>
              Prove what you can actually do.
            </span>
          </h1>

          <p style={{
            fontSize: 'var(--text-lg)',
            color: 'var(--text-secondary)',
            maxWidth: '680px',
            margin: '0 auto var(--space-8) auto',
            lineHeight: 1.7,
          }}>
            Veyra helps anyone discover their ideal vocation, learn through verified free resources, build real-world deliverables, and achieve authentic career readiness across all professions.
          </p>

          <div style={{ display: 'flex', gap: 'var(--space-4)', justifyContent: 'center', flexWrap: 'wrap' }}>
            <a href="/discover" className="btn btn-primary" style={{ padding: '0.875rem 1.75rem', fontSize: 'var(--text-base)' }}>
              Discover Your Career Path
            </a>
            <a href="/careers" className="btn btn-secondary" style={{ padding: '0.875rem 1.75rem', fontSize: 'var(--text-base)' }}>
              Browse 4 Seed Tracks
            </a>
          </div>
        </div>
      </section>

      {/* Seed Careers Section */}
      <section className="container">
        <div style={{ textAlign: 'center', marginBottom: 'var(--space-10)' }}>
          <h2 style={{ marginBottom: 'var(--space-3)' }}>Designed for Every Profession</h2>
          <p style={{ maxWidth: '600px', margin: '0 auto' }}>
            From skilled trades and healthcare to finance and software, Veyra models the real competencies required on the job.
          </p>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
          gap: 'var(--space-6)',
        }}>
          {seedCareers.map((c) => (
            <div key={c.title} className="card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-3)' }}>
                  <span style={{ fontSize: 'var(--text-xs)', fontWeight: 700, color: 'var(--color-primary-600)', textTransform: 'uppercase' }}>
                    {c.category}
                  </span>
                  <span className="badge badge-mastered" style={{ fontSize: '0.7rem' }}>
                    {c.badge}
                  </span>
                </div>
                <h3 style={{ fontSize: 'var(--text-lg)', marginBottom: 'var(--space-2)' }}>{c.title}</h3>
                <p style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)' }}>{c.description}</p>
              </div>

              <div style={{
                marginTop: 'var(--space-4)',
                paddingTop: 'var(--space-4)',
                borderTop: '1px solid var(--border-subtle)',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
              }}>
                <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-tertiary)' }}>Est. {c.duration}</span>
                <a href={`/careers/${c.title.toLowerCase().replace(/[^a-z0-9]+/g, '-')}`} style={{ fontSize: 'var(--text-sm)', fontWeight: 600 }}>
                  Explore Path &rarr;
                </a>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* The Mastery Loop Section */}
      <section style={{ backgroundColor: 'var(--bg-surface-subtle)', padding: 'var(--space-16) 0' }}>
        <div className="container">
          <div style={{ textAlign: 'center', marginBottom: 'var(--space-12)' }}>
            <h2 style={{ marginBottom: 'var(--space-3)' }}>The 6-Step Mastery Loop</h2>
            <p style={{ maxWidth: '600px', margin: '0 auto' }}>
              How Veyra turns ambiguous career goals into demonstrable, job-ready capabilities.
            </p>
          </div>

          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
            gap: 'var(--space-6)',
          }}>
            {loopSteps.map((s) => (
              <div key={s.step} className="card" style={{ backgroundColor: 'var(--bg-surface)' }}>
                <span style={{
                  fontSize: 'var(--text-2xl)',
                  fontWeight: 800,
                  color: 'var(--color-primary-400)',
                  display: 'block',
                  marginBottom: 'var(--space-2)',
                }}>
                  {s.step}
                </span>
                <h4 style={{ marginBottom: 'var(--space-2)' }}>{s.title}</h4>
                <p style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)', margin: 0 }}>
                  {s.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
