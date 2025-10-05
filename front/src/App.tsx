import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ChatProvider } from './context//ChatContext';
import { LanguageProvider } from './context//LanguageContext';
import { Navigation } from './components/layout/Navigation';
import { LandingPage } from './pages/LandingPage';
import { AuthPage } from './pages/AuthPage';
import { ChatPage } from './pages/ChatPage';
import  ProfilePage  from './pages/ProfilePage';

function App() {
  return (
    <LanguageProvider>
      <AuthProvider>
        <ChatProvider>
          <Router>
            <div className="min-h-screen bg-gray-50">
              <Navigation />
              <Routes>
                <Route path="/" element={<LandingPage />} />
                <Route path="/auth" element={<AuthPage />} />
                <Route path="/chat" element={<ChatPage />} />
                <Route path="/profile" element={<ProfilePage />} />
              </Routes>
            </div>
          </Router>
        </ChatProvider>
      </AuthProvider>
    </LanguageProvider>
  );
}

export default App;