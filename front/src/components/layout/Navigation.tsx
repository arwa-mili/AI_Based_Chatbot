import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Menu, X, Globe, LogOut, User, MessageSquare, Home, Bot } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useLanguage } from '../../context/LanguageContext';
import { Button } from '../../components/common/Button';

export const Navigation: React.FC = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { isAuthenticated, user, logout } = useAuth();
  const { language, toggleLanguage, t, isRTL } = useLanguage();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
    setMobileMenuOpen(false);
  };

  return (
    <nav className="bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 hover:opacity-80 transition">
            <Bot className="w-8 h-8" />
            <span className="font-bold text-xl">AI Chat</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-4">
            <Link
              to="/"
              className="flex items-center gap-1 hover:bg-white/20 px-3 py-2 rounded-md transition"
            >
              <Home className="w-4 h-4" />
              <span>{t('nav.home')}</span>
            </Link>

            {isAuthenticated && (
              <>
                <Link
                  to="/chat"
                  className="flex items-center gap-1 hover:bg-white/20 px-3 py-2 rounded-md transition"
                >
                  <MessageSquare className="w-4 h-4" />
                  <span>{t('nav.chat')}</span>
                </Link>
                <Link
                  to="/profile"
                  className="flex items-center gap-1 hover:bg-white/20 px-3 py-2 rounded-md transition"
                >
                  <User className="w-4 h-4" />
                  <span>{t('nav.profile')}</span>
                </Link>
                <button
                  onClick={handleLogout}
                  className="flex items-center gap-1 hover:bg-white/20 px-3 py-2 rounded-md transition"
                >
                  <LogOut className="w-4 h-4" />
                  <span>{t('nav.logout')}</span>
                </button>
              </>
            )}

            {!isAuthenticated && (
              <Link to="/auth">
                <Button variant="secondary" size="sm">
                  {t('nav.login')}
                </Button>
              </Link>
            )}

            <button
              onClick={toggleLanguage}
              className="flex items-center gap-1 hover:bg-white/20 p-2 rounded-md transition"
              title={language === 'en' ? 'العربية' : 'English'}
            >
              <Globe className="w-5 h-5" />
              <span className="text-xs">{language === 'en' ? 'AR' : 'EN'}</span>
            </button>
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 rounded-md hover:bg-white/20 transition"
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Navigation */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-blue-700 border-t border-blue-500">
          <div className="px-2 pt-2 pb-3 space-y-1">
            <Link
              to="/"
              onClick={() => setMobileMenuOpen(false)}
              className="block px-3 py-2 rounded-md hover:bg-white/20 transition"
            >
              {t('nav.home')}
            </Link>

            {isAuthenticated && (
              <>
                <Link
                  to="/chat"
                  onClick={() => setMobileMenuOpen(false)}
                  className="block px-3 py-2 rounded-md hover:bg-white/20 transition"
                >
                  {t('nav.chat')}
                </Link>
                <Link
                  to="/profile"
                  onClick={() => setMobileMenuOpen(false)}
                  className="block px-3 py-2 rounded-md hover:bg-white/20 transition"
                >
                  {t('nav.profile')}
                </Link>
                <button
                  onClick={handleLogout}
                  className="block w-full text-left px-3 py-2 rounded-md hover:bg-white/20 transition"
                >
                  {t('nav.logout')}
                </button>
              </>
            )}

            {!isAuthenticated && (
              <Link
                to="/auth"
                onClick={() => setMobileMenuOpen(false)}
                className="block px-3 py-2 rounded-md hover:bg-white/20 transition"
              >
                {t('nav.login')}
              </Link>
            )}

            <button
              onClick={() => {
                toggleLanguage();
                setMobileMenuOpen(false);
              }}
              className="block w-full text-left px-3 py-2 rounded-md hover:bg-white/20 transition"
            >
              {language === 'en' ? 'العربية' : 'English'}
            </button>
          </div>
        </div>
      )}
    </nav>
  );
};