import { useState } from 'react'
import { getGithubLoginUrl } from '../services/api'

function Landing() {
  const [loading, setLoading] = useState(false)

  const handleGithubLogin = async () => {
    setLoading(true)
    try {
      const response = await getGithubLoginUrl()
      const githubUrl = response.data.url
      // redirect user to GitHub login page
      window.location.href = githubUrl
    } catch (error) {
      console.error('Failed to get GitHub login URL', error)
      setLoading(false)
    }
  }

  return (
    <div style={styles.container}>
      <div style={styles.hero}>
        <h1 style={styles.title}>
          Portfolio Generator
        </h1>
        <p style={styles.subtitle}>
          Connect your GitHub account and get a beautiful 
          portfolio website generated automatically using AI
        </p>
        <div style={styles.features}>
          <div style={styles.feature}>⚡ Pulls all your GitHub repos</div>
          <div style={styles.feature}>🤖 AI writes project descriptions</div>
          <div style={styles.feature}>🚀 Deploy with one click</div>
        </div>
        <button
          style={loading ? styles.buttonLoading : styles.button}
          onClick={handleGithubLogin}
          disabled={loading}
        >
          {loading ? 'Redirecting...' : '🐙 Connect GitHub'}
        </button>
      </div>
    </div>
  )
}

const styles = {
  container: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '100vh',
    padding: '20px'
  },
  hero: {
    textAlign: 'center',
    maxWidth: '600px'
  },
  title: {
    fontSize: '3rem',
    fontWeight: '700',
    marginBottom: '20px',
    background: 'linear-gradient(135deg, #58a6ff, #bf91f3)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent'
  },
  subtitle: {
    fontSize: '1.2rem',
    color: '#8b949e',
    marginBottom: '40px',
    lineHeight: '1.6'
  },
  features: {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
    marginBottom: '40px'
  },
  feature: {
    fontSize: '1rem',
    color: '#e6edf3',
    padding: '12px 20px',
    background: '#161b22',
    borderRadius: '8px',
    border: '1px solid #30363d'
  },
  button: {
    padding: '16px 40px',
    fontSize: '1.1rem',
    fontWeight: '600',
    background: 'linear-gradient(135deg, #238636, #2ea043)',
    color: 'white',
    borderRadius: '8px',
    border: 'none',
    cursor: 'pointer',
    transition: 'opacity 0.2s'
  },
  buttonLoading: {
    padding: '16px 40px',
    fontSize: '1.1rem',
    fontWeight: '600',
    background: '#30363d',
    color: '#8b949e',
    borderRadius: '8px',
    border: 'none',
    cursor: 'not-allowed'
  }
}

export default Landing