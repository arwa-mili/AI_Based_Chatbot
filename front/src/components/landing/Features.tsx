import React from 'react';
import { Bot, Globe, History, Zap, Shield, Sparkles } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';
import { Card } from '../../components/common/Card';

export const Features: React.FC = () => {
  const { t, isRTL } = useLanguage();

  const features = [
    {
      icon: Bot,
      title: t('landing.feature1Title'),
      description: t('landing.feature1Desc'),
      color: 'blue',
    },
    {
      icon: Globe,
      title: t('landing.feature2Title'),
      description: t('landing.feature2Desc'),
      color: 'purple',
    },
    {
      icon: History,
      title: t('landing.feature3Title'),
      description: t('landing.feature3Desc'),
      color: 'pink',
    },
    {
      icon: Zap,
      title:  t('landing.feature4Title'),
      description: t('landing.feature4Desc'),
      color: 'yellow',
    },
    {
      icon: Shield,
      title:  t('landing.feature5Title'),
      description:  t('landing.feature5Desc'),
      color: 'green',
    },
    {
      icon: Sparkles,
      title: t('landing.feature6Title'),
      description:  t('landing.feature6Desc'),
      color: 'indigo',
    },
  ];

  const colorClasses: Record<string, { bg: string; text: string }> = {
    blue: { bg: 'bg-blue-100', text: 'text-blue-600' },
    purple: { bg: 'bg-purple-100', text: 'text-purple-600' },
    pink: { bg: 'bg-pink-100', text: 'text-pink-600' },
    yellow: { bg: 'bg-yellow-100', text: 'text-yellow-600' },
    green: { bg: 'bg-green-100', text: 'text-green-600' },
    indigo: { bg: 'bg-indigo-100', text: 'text-indigo-600' },
  };

  return (
    <div id="features" className="py-20 bg-white">
      <div className={`max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 ${isRTL ? 'rtl' : 'ltr'}`}>
        <h2 className="text-4xl font-bold text-center text-gray-900 mb-4">
          {t('landing.featuresTitle')}
        </h2>
        <p className="text-center text-gray-600 mb-12 max-w-2xl mx-auto">
          {t('landing.featuresDescription')}
        </p>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            const colors = colorClasses[feature.color];

            return (
              <Card key={index} hover className="group">
                <div className={`w-12 h-12 ${colors.bg} rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                  <Icon className={`w-6 h-6 ${colors.text}`} />
                </div>
                <h3 className="text-xl font-bold mb-2 text-gray-900">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </Card>
            );
          })}
        </div>
      </div>
    </div>
  );
};