import React from 'react';
import { Sparkles } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

interface AISummaryProps {
  summary?: string;
}

export const AISummary: React.FC<AISummaryProps> = ({ summary }) => {
  const { t } = useLanguage();

  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center space-x-2">
        <Sparkles className="w-4 h-4" />
        <span>{t('profile.aiSummary')}</span>
      </label>
      <div className="px-4 py-4 bg-gradient-to-br from-blue-50 to-purple-50 rounded-lg border border-blue-200">
        {summary ? (
          <p className="text-gray-700 leading-relaxed">{summary}</p>
        ) : (
          <p className="text-gray-500 italic">{t('profile.noSummary')}</p>
        )}
      </div>
    </div>
  );
};
