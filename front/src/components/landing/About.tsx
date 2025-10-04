import React from 'react';
import { useLanguage } from '../../context/LanguageContext';

export const About: React.FC = () => {
  const { t, isRTL } = useLanguage();

  return (
    <div className="py-20 bg-gradient-to-br from-gray-50 to-gray-100">
      <div className={`max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 ${isRTL ? 'rtl text-right' : 'ltr text-left'}`}>
        <h2 className="text-4xl font-bold text-gray-900 mb-6 text-center">
          {t('landing.aboutTitle')}
        </h2>
        <p className="text-lg text-gray-600 leading-relaxed text-center mb-8">
          {t('landing.aboutDesc')}
        </p>
        <div className="bg-white p-8 rounded-xl shadow-lg">
          <p className="text-gray-700 leading-relaxed mb-4">
            Our platform integrates cutting-edge AI models to provide you with intelligent, context-aware responses. 
            Whether you are seeking information, creative inspiration, or technical assistance, our chatbot adapts to your needs.
          </p>
          <p className="text-gray-700 leading-relaxed">
            Built with modern technologies including React, TypeScript, and Tailwind CSS, our application ensures 
            a smooth, responsive experience across all devices. Your chat history is securely stored, and our AI 
            generates personalized summaries to enhance future interactions.
          </p>
        </div>
      </div>
    </div>
  );
};