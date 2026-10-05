import type { Metadata } from 'next';
import '../styles/globals.css';

export const metadata: Metadata = {
  title: 'Veyra — Career Learning & Mastery for All Professions',
  description: 'Discover your path, learn from verified free resources, build authentic projects, and become career-ready across technology, healthcare, trades, finance, and more.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>
        <header style={{
          borderBottom: '1px solid var(--border-subtle)',
          backgroundColor: 'var(--bg-surface)',
          position: 'sticky',
          top: 0,
          zIndex: 40,
        }}>
          <div className="container" style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            height: '4.5rem',
          }}>
            <a href="/" style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.625rem',
              fontWeight: 800,
              fontSize: 'var(--text-xl)',
              color: 'var(--text-primary)',
              textDecoration: 'none',
            }}>
              <span style={{
                display: 'inline-flex',
                alignItems: 'center',
                justifyContent: 'center',
                width: '2rem',
                height: '2rem',
                borderRadius: 'var(--radius-md)',
                background: 'linear-gradient(135deg, var(--color-primary-600), var(--color-accent-600))',
                color: '#fff',
                fontSize: 'var(--text-sm)',
                fontWeight: 800,
              }}>
                V
              </span>
              Veyra
            </a>

            <nav style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-6)' }}>
              <a href="/careers" style={{ fontWeight: 500, color: 'var(--text-secondary)' }}>Careers</a>
              <a href="/discover" style={{ fontWeight: 500, color: 'var(--text-secondary)' }}>Discovery</a>
              <a href="/how-it-works" style={{ fontWeight: 500, color: 'var(--text-secondary)' }}>How it Works</a>
              <a href="/discover" className="btn btn-primary" style={{ padding: '0.5rem 1rem' }}>
                Start Free
              </a>
            </nav>
          </div>
        </header>

        <main style={{ flex: 1 }}>
          {children}
        </main>

        <footer style={{
          borderTop: '1px solid var(--border-subtle)',
          backgroundColor: 'var(--bg-surface)',
          paddingTop: 'var(--space-10)',
          paddingBottom: 'var(--space-10)',
          marginTop: 'var(--space-16)',
        }}>
          <div className="container" style={{
            display: 'flex',
            flexDirection: 'column',
            gap: 'var(--space-6)',
            alignItems: 'center',
            textAlign: 'center',
          }}>
            <p style={{ color: 'var(--text-tertiary)', fontSize: 'var(--text-sm)', margin: 0 }}>
              &copy; {new Date().getFullYear()} Veyra. 100% Free, Career-Agnostic Mastery Learning.
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
