import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useLanguage } from '../../context/LanguageContext';
import { useAuth } from '../../context/AuthContext';
import { Button } from '../../components/common/Button';
import { ArrowRight, Sparkles } from 'lucide-react';

export const Hero: React.FC = () => {
  const { t, isRTL } = useLanguage();
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className={`text-center ${isRTL ? 'rtl' : 'ltr'}`}>
          {/* Badge */}
          <div className="inline-flex items-center space-x-2 bg-blue-100 text-blue-700 px-4 py-2 rounded-full mb-6">
            <Sparkles className="w-4 h-4" />
            <span className="text-sm font-semibold">AI-Powered Conversations</span>
          </div>

          {/* Title */}
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight">
            {t('landing.heroTitle')}
          </h1>

          {/* Subtitle */}
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto leading-relaxed">
            {t('landing.heroSubtitle')}
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row justify-center items-center space-y-4 sm:space-y-0 sm:space-x-4">
            <Button
              onClick={() => navigate(isAuthenticated ? '/chat' : '/auth')}
              size="lg"
              icon={ArrowRight}
              className="w-full sm:w-auto"
            >
              {t('landing.getStarted')}
            </Button>
            <Button
              variant="secondary"
              size="lg"
              className="w-full sm:w-auto"
              onClick={() => document.getElementById('features')?.scrollIntoView({ behavior: 'smooth' })}
            >
              {t('landing.learnMore')}
            </Button>
          </div>

          {/* Stats */}
          <div className="mt-16 grid grid-cols-3 gap-8 max-w-2xl mx-auto">
            <div>
              <div className="text-4xl font-bold text-blue-600">3</div>
              <div className="text-sm text-gray-600 mt-1">AI Models</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-purple-600">2</div>
              <div className="text-sm text-gray-600 mt-1">Languages</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-pink-600">∞</div>
              <div className="text-sm text-gray-600 mt-1">Possibilities</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};