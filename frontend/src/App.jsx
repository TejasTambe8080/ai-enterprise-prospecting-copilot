import React from 'react';

function App() {
  return (
    <div style={{ 
      minHeight: '100vh', 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      fontFamily: 'Arial, sans-serif'
    }}>
      <div style={{
        background: 'white',
        padding: '40px',
        borderRadius: '20px',
        textAlign: 'center',
        boxShadow: '0 20px 60px rgba(0,0,0,0.3)'
      }}>
        <h1 style={{ color: '#6366f1' }}>🚀 FlytBase BDR System</h1>
        <p style={{ color: '#666', fontSize: '18px' }}>Your system is running!</p>
        <p style={{ color: '#999', fontSize: '14px' }}>React is rendering correctly.</p>
      </div>
    </div>
  );
}

export default App;