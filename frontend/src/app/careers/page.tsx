'use client';

import { useEffect, useState } from 'react';
import { api, CareerListItem } from '@/lib/api';

export default function CareersPage() {
  const [careers, setCareers] = useState<CareerListItem[]>([]);
  const [selectedCategory, setSelectedCategory] = useState('ALL');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function loadCareers() {
      try {
        const data = await api.listCareers();
        setCareers(data);
      } catch (err: any) {
        setError(err.message || 'Could not load career paths.');
      } finally {
        setIsLoading(false);
      }
    }
    loadCareers();
  }, []);

  const categories = ['ALL', ...Array.from(new Set(careers.map((c) => c.industry_category)))];

  const filteredCareers = selectedCategory === 'ALL'
    ? careers
    : careers.filter((c) => c.industry_category === selectedCategory);

  return (
    <div className="container" style={{ paddingTop: 'var(--space-12)', paddingBottom: 'var(--space-16)' }}>
      {/* Title */}
      <div style={{ textAlign: 'center', marginBottom: 'var(--space-10)' }}>
        <span style={{
          fontSize: 'var(--text-xs)',
          fontWeight: 700,
          color: 'var(--color-primary-600)',
          textTransform: 'uppercase',
          letterSpacing: '0.05em',
        }}>
          Career Catalog
        </span>
        <h1 style={{ fontSize: 'var(--text-3xl)', marginTop: 'var(--space-2)', marginBottom: 'var(--space-3)' }}>
          Explore Structured Career Pathways
        </h1>
        <p style={{ color: 'var(--text-secondary)', maxWidth: '600px', margin: '0 auto' }}>
          Every career track is broken down into verifiable competencies, skills, prerequisite graphs, and free verified learning resources.
        </p>
      </div>

      {/* Category Filter Pills */}
      <div style={{ display: 'flex', justifyContent: 'center', gap: 'var(--space-2)', flexWrap: 'wrap', marginBottom: 'var(--space-8)' }}>
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            style={{
              padding: 'var(--space-2) var(--space-4)',
              borderRadius: 'var(--radius-full)',
              border: selectedCategory === cat ? '1px solid var(--color-primary-600)' : '1px solid var(--border-default)',
              backgroundColor: selectedCategory === cat ? 'var(--color-primary-600)' : 'var(--bg-surface)',
              color: selectedCategory === cat ? '#ffffff' : 'var(--text-secondary)',
              fontWeight: 600,
              fontSize: 'var(--text-xs)',
              cursor: 'pointer',
              transition: 'all var(--transition-fast)',
            }}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Error / Loading */}
      {error && (
        <div style={{
          backgroundColor: '#fef2f2',
          border: '1px solid #fecaca',
          color: '#991b1b',
          padding: 'var(--space-4)',
          borderRadius: 'var(--radius-md)',
          textAlign: 'center',
          maxWidth: '600px',
          margin: '0 auto var(--space-8) auto',
        }}>
          {error}
        </div>
      )}

      {isLoading ? (
        <div style={{ textAlign: 'center', padding: 'var(--space-16) 0', color: 'var(--text-tertiary)' }}>
          Loading career tracks...
        </div>
      ) : (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
          gap: 'var(--space-6)',
        }}>
          {filteredCareers.map((career) => (
            <div key={career.id} className="card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-3)' }}>
                  <span style={{ fontSize: 'var(--text-xs)', fontWeight: 700, color: 'var(--color-primary-600)', textTransform: 'uppercase' }}>
                    {career.industry_category}
                  </span>
                  <span className="badge badge-mastered">
                    {career.badge}
                  </span>
                </div>

                <h2 style={{ fontSize: 'var(--text-xl)', marginBottom: 'var(--space-2)' }}>{career.title}</h2>
                <p style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
                  {career.description}
                </p>
              </div>

              <div style={{
                marginTop: 'var(--space-6)',
                paddingTop: 'var(--space-4)',
                borderTop: '1px solid var(--border-subtle)',
              }}>
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  fontSize: 'var(--text-xs)',
                  color: 'var(--text-secondary)',
                  marginBottom: 'var(--space-4)',
                }}>
                  <span>{career.total_skills} Core Skills</span>
                  <span>Est. {career.total_estimated_hours}h of Practice</span>
                  <span>~{career.avg_months_to_complete} Months</span>
                </div>

                <a
                  href={`/careers/${career.slug}`}
                  className="btn btn-primary"
                  style={{ width: '100%', boxSizing: 'border-box' }}
                >
                  View Full Curriculum &amp; DAG &rarr;
                </a>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
