import React from 'react';
import { Sparkles } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

interface AISummaryProps {
  summary?: string;
}

export const AISummary: React.FC<AISummaryProps> = ({ summary }) => {
  const { t } = useLanguage();

  return (
    <div className="relative rounded-xl border border-blue-200 bg-gradient-to-br from-blue-50 to-purple-50 p-5 shadow-sm hover:shadow-md transition-all duration-300">
      <div className="flex items-center mb-3 gap-2">
        <Sparkles className="w-5 h-5 text-blue-500" />
        <span className="font-semibold text-gray-800">{t('profile.aiSummary')}</span>
      </div>
      {summary ? (
        <p className="text-gray-700 leading-relaxed">{summary}</p>
      ) : (
        <p className="text-gray-500 italic">{t('profile.noSummary')}</p>
      )}
    </div>
  );
};
