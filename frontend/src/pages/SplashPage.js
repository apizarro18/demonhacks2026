import React from 'react';
import { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
  

const SplashPage = () => {
    
  return (
    
    <div style={styles.splashContainer}>
      {/* Animated Shield Icon */}
      <div className="pulse-container" style={styles.logoCircle}>
        <span style={{ fontSize: '60px' }}>🛡️</span>
      </div>

      <h1 style={styles.title}>SAFE BLUE</h1>
      
      {/* Progress Bar Visual */}
      <div style={styles.loaderBar}>
        <div className="loader-fill"></div>
      </div>

      <p style={styles.subtitle}>SECURE CONNECTION ESTABLISHED</p>

      {/* Scoped CSS for the Splash Animations */}
      <style>{`
        @keyframes pulse {
          0% { transform: scale(1); opacity: 0.8; box-shadow: 0 0 0 0 rgba(99, 179, 237, 0.4); }
          50% { transform: scale(1.05); opacity: 1; box-shadow: 0 0 20px 10px rgba(99, 179, 237, 0); }
          100% { transform: scale(1); opacity: 0.8; }
        }
        @keyframes fill {
          0% { width: 0%; }
          100% { width: 100%; }
        }
        .pulse-container { 
          animation: pulse 2s infinite ease-in-out; 
        }
        .loader-fill { 
          height: 100%; 
          background-color: #63B3ED; 
          animation: fill 2.5s ease-in-out; 
          width: 100%;
        }
      `}</style>
    </div>
  );
};

const styles = {
  splashContainer: {
    height: '100vh',
    width: '100vw',
    backgroundColor: '#1A2B48', // Safe Blue Brand Color
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    color: 'white',
    fontFamily: '"Segoe UI", Tahoma, Geneva, Verdana, sans-serif',
    position: 'fixed',
    top: 0,
    left: 0,
    zIndex: 9999,
  },
  logoCircle: {
    width: '140px',
    height: '140px',
    borderRadius: '70px',
    backgroundColor: 'rgba(255,255,255,0.05)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: '30px',
    border: '1px solid rgba(99, 179, 237, 0.3)',
  },
  title: {
    letterSpacing: '10px',
    fontSize: '2.8rem',
    fontWeight: '900',
    margin: '0',
    textAlign: 'center',
  },
  loaderBar: {
    width: '240px',
    height: '3px',
    backgroundColor: 'rgba(255,255,255,0.1)',
    marginTop: '40px',
    borderRadius: '10px',
    overflow: 'hidden',
  },
  subtitle: {
    color: '#63B3ED',
    marginTop: '20px',
    fontSize: '12px',
    letterSpacing: '2px',
    fontWeight: 'bold',
  }
};

export default SplashPage;