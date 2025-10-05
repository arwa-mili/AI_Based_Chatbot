import React, { useEffect, useState } from 'react';
import { Sparkles } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';
import { getUserSummary } from '../../services/profileService';
import { GetLastSummaryResponse } from '../../types/profile.types';

export const AISummary: React.FC = () => {
  const { t } = useLanguage();
  const [summary, setSummary] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        setLoading(true);
        setError(null);
        const res = await getUserSummary();
        setSummary(res.data?.summary ?? null);
      } catch (err) {
        console.error(err);
        setError(t('profile.failedToLoadSummary'));
      } finally {
        setLoading(false);
      }
    };
    fetchSummary();
  }, [t]);

  if (loading) return <p className="text-gray-500 italic">Loading summary...</p>;
  if (error) return <p className="text-red-500">{error}</p>;

  return (
    <div className="relative rounded-xl border border-blue-200 bg-gradient-to-br from-blue-50 to-purple-50 p-5 shadow-sm hover:shadow-md transition-all duration-300">
      <div className="flex items-center mb-3 gap-2">
        <Sparkles className="w-5 h-5 text-blue-500" />
        <span className="font-semibold text-gray-800">{t('profile.aiSummary')}</span>
      </div>
      <p className="text-gray-700 leading-relaxed">{summary ?? t('profile.noSummary')}</p>
    </div>
  );
};
