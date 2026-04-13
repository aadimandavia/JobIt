import { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../hooks/useAuth';
import { fetchJobs } from '../services/api';

const FILTER_OPTIONS = [
  { label: 'All', keyword: '' },
  { label: 'Python', keyword: 'python' },
  { label: 'React', keyword: 'react' },
  { label: 'Remote', keyword: 'remote' },
  { label: 'Internship', keyword: 'intern' },
  { label: 'Frontend', keyword: 'frontend' },
  { label: 'Backend', keyword: 'backend' },
  { label: 'DevOps', keyword: 'devops' },
];

function timeAgo(dateStr) {
  const now = new Date();
  const date = new Date(dateStr);
  const seconds = Math.floor((now - date) / 1000);

  if (seconds < 60) return 'just now';
  if (seconds < 3600) return Math.floor(seconds / 60) + 'm ago';
  if (seconds < 86400) return Math.floor(seconds / 3600) + 'h ago';
  if (seconds < 604800) return Math.floor(seconds / 86400) + 'd ago';
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

function SkeletonCards() {
  return Array.from({ length: 6 }).map((_, i) => (
    <div className="skeleton-card" key={i}>
      <div className="skeleton-line wide"></div>
      <div className="skeleton-line medium"></div>
      <div className="skeleton-line wide"></div>
      <div className="skeleton-line short"></div>
      <div className="skeleton-line xs"></div>
    </div>
  ));
}

function JobCard({ job, index }) {
  const desc = job.description
    ? job.description.substring(0, 250) + (job.description.length > 250 ? '...' : '')
    : 'No description available.';

  return (
    <div
      className="job-card"
      style={{ animationDelay: `${index * 60}ms` }}
      onClick={() => window.open(job.url, '_blank')}
    >
      <div className="job-header">
        <div className="job-title">{job.title}</div>
        <div className="job-badge-row">
          {job.subreddit && <span className="job-badge">r/{job.subreddit}</span>}
          {job.stipend && <div className="job-stipend">{job.stipend}</div>}
        </div>
      </div>
      <div className="job-description">{desc}</div>
      <div className="job-footer">
        <div className="job-meta">
          <span className="meta-item">🕐 {timeAgo(job.created_at)}</span>
        </div>
        <a
          href={job.url}
          target="_blank"
          rel="noopener noreferrer"
          className="job-link"
          onClick={e => e.stopPropagation()}
        >
          View Details →
        </a>
      </div>
    </div>
  );
}

export default function DashboardPage({ theme, toggleTheme }) {
  const { user, handleLogout } = useAuth();
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [keyword, setKeyword] = useState('');
  const [searchInput, setSearchInput] = useState('');
  const [limit, setLimit] = useState(20);
  const [activeFilter, setActiveFilter] = useState('');

  const loadJobs = useCallback(async () => {
    setLoading(true);
    setError(false);
    try {
      const data = await fetchJobs(limit, keyword);
      setJobs(data);
    } catch {
      setError(true);
    } finally {
      setLoading(false);
    }
  }, [limit, keyword]);

  useEffect(() => {
    loadJobs();
  }, [loadJobs]);

  function handleSearch() {
    const val = searchInput.trim();
    setKeyword(val);
    setLimit(20);
    setActiveFilter(val.toLowerCase());
  }

  function handleFilterClick(kw) {
    setSearchInput(kw);
    setKeyword(kw);
    setLimit(20);
    setActiveFilter(kw);
  }

  function handleLoadMore() {
    setLimit(prev => prev + 20);
  }

  const ThemeIcon = theme === 'light' ? '🌙' : '☀️';
  const totalJobs = jobs.length;
  const paidJobs = jobs.filter(j => j.stipend).length;

  return (
    <div className="dashboard">
      {/* Navbar */}
      <nav className="navbar">
        <div className="navbar-brand">
          <img src="/logo.png" alt="JobIt Logo" className="nav-logo-img" />
          <h2>JobIt</h2>
        </div>
        <div className="navbar-user">
          <button 
            className="btn-theme-toggle" 
            onClick={toggleTheme} 
            title={`Switch to ${theme === 'light' ? 'Dark' : 'Light'} mode`}
          >
            {ThemeIcon}
          </button>
          <div className="user-info">
            <div className="user-name">{user?.name || 'User'}</div>
            <div className="user-phone">{user?.email || user?.phone}</div>
          </div>
          <div className="user-avatar">{(user?.name || user?.email || 'U').charAt(0).toUpperCase()}</div>
          <button className="btn-logout" onClick={handleLogout}>Logout</button>
        </div>
      </nav>

      {/* Hero */}
      <section className="hero-section">
        <h1>Find Your Next <span>Opportunity</span></h1>
        <p>Real-time job listings aggregated from Reddit's top hiring communities</p>

        <div className="stats-row">
          <div className="stat-card">
            <div className="stat-value">{loading ? '—' : totalJobs}</div>
            <div className="stat-label">Total Jobs</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">10</div>
            <div className="stat-label">Subreddits</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{loading ? '—' : paidJobs}</div>
            <div className="stat-label">Paid Listings</div>
          </div>
        </div>
      </section>

      {/* Search */}
      <section className="search-section">
        <div className="search-bar">
          <div className="search-input-wrapper">
            <span className="search-icon">🔍</span>
            <input
              type="text"
              id="searchInput"
              placeholder="Search jobs by keyword... (e.g., Python, React, Remote)"
              autoComplete="off"
              value={searchInput}
              onChange={e => setSearchInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleSearch()}
            />
          </div>
          <button className="btn-search" onClick={handleSearch}>Search</button>
        </div>
        <div className="filter-pills">
          {FILTER_OPTIONS.map(opt => (
            <button
              key={opt.keyword}
              className={`filter-pill ${activeFilter === opt.keyword ? 'active' : ''}`}
              onClick={() => handleFilterClick(opt.keyword)}
            >
              {opt.label}
            </button>
          ))}
        </div>
      </section>

      {/* Jobs Grid */}
      <div className="jobs-grid" id="jobsGrid">
        {loading ? (
          <SkeletonCards />
        ) : error ? (
          <div className="empty-state">
            <div className="empty-icon">⚠️</div>
            <h3>Failed to load jobs</h3>
            <p>Please check your connection and try again.</p>
          </div>
        ) : jobs.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">🔍</div>
            <h3>No jobs found</h3>
            <p>Try a different keyword or check back later for new listings.</p>
          </div>
        ) : (
          jobs.map((job, index) => (
            <JobCard key={job.url + index} job={job} index={index} />
          ))
        )}
      </div>

      {/* Load More */}
      {!loading && !error && jobs.length >= limit && (
        <div className="load-more-section">
          <button className="btn-load-more" onClick={handleLoadMore}>Load More Jobs</button>
        </div>
      )}

      {/* Footer */}
      <footer className="footer">
        <div className="footer-content">
          <div className="footer-info">
            <p>
              JobIt — Aggregating opportunities from{' '}
              <a href="https://reddit.com" target="_blank" rel="noopener noreferrer">Reddit</a>{' '}
              in real-time 🚀
            </p>
          </div>
          <div className="footer-divider"></div>
          <div className="developer-section">
            <h4>Developed by Aadi Mandavia</h4>
            <div className="dev-links">
              <a href="https://github.com/aadimandavia" target="_blank" rel="noopener noreferrer" className="dev-link">
                <span className="link-icon">GitHub</span>
              </a>
              <a href="https://linkedin.com/in/aadi-mandavia-006571259" target="_blank" rel="noopener noreferrer" className="dev-link">
                <span className="link-icon">LinkedIn</span>
              </a>
              <a href="mailto:aadim2612@gmail.com" className="dev-link">
                <span className="link-icon">Email</span>
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
