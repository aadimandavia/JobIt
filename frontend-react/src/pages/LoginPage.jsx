import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { sendOtp, verifyOtp, registerManual, loginManual } from '../services/api';
import { useAuth } from '../hooks/useAuth';

function StatusMessage({ message, type }) {
  if (!message) return null;
  return <div className={`status-message ${type}`}>{message}</div>;
}

function OtpInputGroup({ onComplete, resetKey }) {
  const inputs = useRef([]);
  const [values, setValues] = useState(Array(6).fill(''));

  useEffect(() => {
    setValues(Array(6).fill(''));
    inputs.current[0]?.focus();
  }, [resetKey]);

  function handleChange(index, val) {
    if (!/^\d?$/.test(val)) return;
    const next = [...values];
    next[index] = val;
    setValues(next);

    if (val && index < 5) {
      inputs.current[index + 1]?.focus();
    }

    const otp = next.join('');
    if (otp.length === 6 && next.every(v => v)) {
      onComplete(otp);
    }
  }

  function handleKeyDown(index, e) {
    if (e.key === 'Backspace' && !values[index] && index > 0) {
      const next = [...values];
      next[index - 1] = '';
      setValues(next);
      inputs.current[index - 1]?.focus();
    }
  }

  return (
    <div className="otp-inputs">
      {values.map((val, i) => (
        <input
          key={i}
          ref={el => (inputs.current[i] = el)}
          type="text"
          maxLength={1}
          inputMode="numeric"
          value={val}
          className={val ? 'filled' : ''}
          onChange={e => handleChange(i, e.target.value)}
          onKeyDown={e => handleKeyDown(i, e)}
        />
      ))}
    </div>
  );
}

export default function LoginPage({ theme, toggleTheme }) {
  const navigate = useNavigate();
  const { loginUser } = useAuth();

  const [authMode, setAuthMode] = useState('login'); // 'login' | 'register' | 'otp'
  const [step, setStep] = useState('input'); // 'input' | 'verify' (for OTP)
  
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  
  const [status, setStatus] = useState({ message: '', type: '' });
  const [loading, setLoading] = useState(false);
  const [otpResetKey, setOtpResetKey] = useState(0);
  const [timer, setTimer] = useState(0);

  useEffect(() => {
    if (timer <= 0) return;
    const id = setInterval(() => setTimer(t => t - 1), 1000);
    return () => clearInterval(id);
  }, [timer]);

  function showStatus(message, type = 'error') {
    setStatus({ message, type });
    setTimeout(() => setStatus({ message: '', type: '' }), 5000);
  }

  async function handleManualLogin() {
    if (!email || !password) {
      showStatus('Please enter both email and password');
      return;
    }
    setLoading(true);
    try {
      const data = await loginManual(email, password);
      if (data.success) {
        showStatus('Login successful!', 'success');
        loginUser(data.user, data.access_token);
        setTimeout(() => navigate('/dashboard'), 600);
      } else {
        showStatus(data.message || 'Invalid credentials');
      }
    } catch {
      showStatus('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  }

  async function handleManualRegister() {
    if (!email || !password) {
      showStatus('Email and password are required');
      return;
    }
    setLoading(true);
    try {
      const data = await registerManual(email, password, name);
      if (data.success) {
        showStatus('Account created! Logging you in...', 'success');
        loginUser(data.user, data.access_token);
        setTimeout(() => navigate('/dashboard'), 1000);
      } else {
        showStatus(data.message || 'Registration failed');
      }
    } catch {
      showStatus('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  }

  async function handleSendOTP() {
    if (!phone || phone.length < 10) {
      showStatus('Enter a valid phone number');
      return;
    }
    setLoading(true);
    try {
      const data = await sendOtp(phone);
      if (data.success) {
        showStatus('OTP sent!', 'success');
        setStep('verify');
        setTimer(30);
      } else {
        showStatus(data.message || 'Failed to send OTP');
      }
    } catch {
      showStatus('Network error.');
    } finally {
      setLoading(false);
    }
  }

  async function handleVerifyOTP(otp) {
    setLoading(true);
    try {
      const data = await verifyOtp(phone, otp);
      if (data.success) {
        showStatus('Login successful!', 'success');
        loginUser(data.user, data.access_token);
        setTimeout(() => navigate('/dashboard'), 600);
      } else {
        showStatus(data.message || 'Invalid OTP');
        setOtpResetKey(k => k + 1);
      }
    } catch {
      showStatus('Network error.');
    } finally {
      setLoading(false);
    }
  }

  const handleGoogleLogin = () => {
    const apiBase = import.meta.env.VITE_API_URL || '';
    window.location.href = `${apiBase}/auth/google/login`;
  };

  const ThemeIcon = theme === 'light' ? '🌙' : '☀️';

  return (
    <div className="auth-container">
      <div className="auth-card">
        <button className="btn-theme-toggle" onClick={toggleTheme} style={{ position: 'absolute', top: '24px', right: '24px' }}>
          {ThemeIcon}
        </button>

        <div className="auth-logo">
          <img src="/logo.png" alt="JobIt Logo" className="logo-img" />
          <h1>JobIt</h1>
          <p>Find your next role with Google, Email or Phone</p>
        </div>

        <div className="auth-tabs">
          <button className={`auth-tab ${authMode === 'login' ? 'active' : ''}`} onClick={() => setAuthMode('login')}>Login</button>
          <button className={`auth-tab ${authMode === 'register' ? 'active' : ''}`} onClick={() => setAuthMode('register')}>Register</button>
          <button className={`auth-tab ${authMode === 'otp' ? 'active' : ''}`} onClick={() => setAuthMode('otp')}>Phone</button>
        </div>

        <StatusMessage message={status.message} type={status.type} />

        {authMode === 'login' && (
          <div className="auth-step">
            <div className="form-group">
              <label>Email Address</label>
              <div className="input-wrapper">
                <input type="email" placeholder="name@example.com" value={email} onChange={e => setEmail(e.target.value)} onKeyDown={e => e.key === 'Enter' && handleManualLogin()} />
                <span className="input-icon">✉️</span>
              </div>
            </div>
            <div className="form-group">
              <label>Password</label>
              <div className="input-wrapper">
                <input type="password" placeholder="••••••••" value={password} onChange={e => setPassword(e.target.value)} onKeyDown={e => e.key === 'Enter' && handleManualLogin()} />
                <span className="input-icon">🔒</span>
              </div>
            </div>
            <button className="btn btn-primary" onClick={handleManualLogin} disabled={loading}>
              {loading ? <span className="spinner"></span> : 'Sign In'}
            </button>
          </div>
        )}

        {authMode === 'register' && (
          <div className="auth-step">
            <div className="form-group">
              <label>Full Name</label>
              <div className="input-wrapper">
                <input type="text" placeholder="John Doe" value={name} onChange={e => setName(e.target.value)} />
                <span className="input-icon">👤</span>
              </div>
            </div>
            <div className="form-group">
              <label>Email Address</label>
              <div className="input-wrapper">
                <input type="email" placeholder="name@example.com" value={email} onChange={e => setEmail(e.target.value)} />
                <span className="input-icon">✉️</span>
              </div>
            </div>
            <div className="form-group">
              <label>Password</label>
              <div className="input-wrapper">
                <input type="password" placeholder="Create a password" value={password} onChange={e => setPassword(e.target.value)} />
                <span className="input-icon">🔒</span>
              </div>
            </div>
            <button className="btn btn-primary" onClick={handleManualRegister} disabled={loading}>
              {loading ? <span className="spinner"></span> : 'Create Account'}
            </button>
          </div>
        )}

        {authMode === 'otp' && (
          <div className="auth-step">
            {step === 'input' ? (
              <>
                <div className="form-group">
                  <label>Phone Number</label>
                  <div className="input-wrapper">
                    <input type="tel" placeholder="+91 98765 43210" value={phone} onChange={e => setPhone(e.target.value)} />
                    <span className="input-icon">📱</span>
                  </div>
                </div>
                <button className="btn btn-primary" onClick={handleSendOTP} disabled={loading}>
                  {loading ? <span className="spinner"></span> : 'Send OTP'}
                </button>
              </>
            ) : (
              <>
                <div className="form-group">
                  <label>Verification Code</label>
                  <OtpInputGroup onComplete={handleVerifyOTP} resetKey={otpResetKey} />
                </div>
                <div className="resend-row">
                  {timer > 0 ? <span>Resend in {timer}s</span> : <button className="link-btn" onClick={handleSendOTP}>Resend Code</button>}
                </div>
                <button className="btn btn-outline" style={{ marginTop: '16px' }} onClick={() => setStep('input')}>← Back</button>
              </>
            )}
          </div>
        )}

        <div className="oauth-divider">OR</div>

        <button className="btn btn-google" onClick={handleGoogleLogin}>
          <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" alt="Google" className="google-icon" />
          Continue with Google
        </button>
      </div>
    </div>
  );
}
