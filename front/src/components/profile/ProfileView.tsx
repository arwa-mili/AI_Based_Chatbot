import React, { useEffect, useState } from 'react';
import { User, History } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';
import { ProfileStats } from './ProfileStats';
import { AISummary } from './AISummary';
import { Card } from '../../components/common/Card';
import { Dialog } from 'primereact/dialog';
import { Button } from 'primereact/button';
import { ProgressSpinner } from 'primereact/progressspinner';
import { GetProfile, GetLastSummaryResponse } from '../../types/profile.types';

interface OldSummary {
  summary: string;
  last_updated: string;
}

interface ProfileViewProps {
  profile: GetProfile;
  summary?: GetLastSummaryResponse | null;
}

export const ProfileView: React.FC<ProfileViewProps> = ({ profile, summary }) => {
  const { t, language, isRTL } = useLanguage();
  const [oldSummaries, setOldSummaries] = useState<OldSummary[]>([]);
  const [showDialog, setShowDialog] = useState(false);

  useEffect(() => {
    if (summary) {
      setOldSummaries([
        summary,
        {
          summary: 'This user has shown remarkable improvement in project structuring.',
          last_updated: '2024-09-10',
        },
        {
          summary: 'Very consistent communication and problem-solving approach.',
          last_updated: '2024-08-22',
        },
      ]);
    }
  }, [summary]);

  return (
    <div className={`min-h-[calc(100vh-4rem)] bg-gray-50 py-8 ${isRTL ? 'rtl' : 'ltr'}`}>
      <div className="max-w-4xl mx-auto px-4">
        <Card>
          {/* Header */}
          <div className="flex items-center gap-4 mb-8 pb-6 border-b border-gray-200">
            <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center shadow-lg">
              <User className="w-10 h-10 text-white" />
            </div>
            <div className="flex-1">
              <h2 className="text-3xl font-bold text-gray-900">{t('profile.title')}</h2>
              <p className="text-gray-600">{profile.email}</p>
            </div>
          </div>

          {/* Profile Information */}
          <div className="space-y-6">
            {/* Name */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">{t('auth.name')}</label>
              <div className="px-4 py-3 bg-gray-50 rounded-lg border border-gray-200">{profile.name}</div>
            </div>

            {/* Email */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">{t('auth.email')}</label>
              <div className="px-4 py-3 bg-gray-50 rounded-lg border border-gray-200">{profile.email}</div>
            </div>


            {/* Member Since */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">{t('profile.memberSince')}</label>
              <div className="px-4 py-3 bg-gray-50 rounded-lg border border-gray-200">
                {new Date(profile.created_at).toLocaleDateString(language === 'en' ? 'en-US' : 'ar-SA', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                })}
              </div>
            </div>

            {/* AI Summary with Button */}
            <div className="relative">
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-gray-700 flex items-center gap-2">
                  🪄 {t('profile.aiSummary')}
                </span>
                <Button
                  icon={<History size={16} />}
                  label={t('profile.oldSummaries')}
                  className="p-button-text p-button-sm"
                  onClick={() => setShowDialog(true)}
                />
              </div>
              <AISummary summary={summary?.summary} />
            </div>

            {/* Stats */}
            <ProfileStats />
          </div>
        </Card>
      </div>

      {/* Dialog for Old Summaries */}
      <Dialog
        header={t('profile.oldSummaries')}
        visible={showDialog}
        style={{ width: '40vw' }}
        onHide={() => setShowDialog(false)}
      >
        <div className="space-y-4">
          {oldSummaries.map((item, idx) => (
            <div
              key={idx}
              className="p-4 bg-gray-50 rounded-lg border border-gray-200 shadow-sm hover:bg-gray-100 transition-all"
            >
              <p className="text-gray-800 leading-relaxed mb-2">{item.summary}</p>
              <p className="text-xs text-gray-500">
                {new Date(item.last_updated).toLocaleDateString(language === 'en' ? 'en-US' : 'ar-SA')}
              </p>
            </div>
          ))}
        </div>
      </Dialog>
    </div>
  );
};
