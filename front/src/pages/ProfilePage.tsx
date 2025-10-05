import React, { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { ProfileView } from '../components/profile/ProfileView';
import { GetProfile } from '../types/profile.types';
import { getProfileInfo } from '../services/profileService';

const ProfilePage: React.FC = () => {
  const { isAuthenticated, isLoading: authLoading } = useAuth();
  const { language } = useLanguage(); 
  const [profile, setProfile] = useState<GetProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadProfileData = async () => {
    try {
      setLoading(true);
      setError(null);
      const profileRes = await getProfileInfo();
      setProfile(profileRes.data);
    } catch (err) {
      console.error(err);
      setError('Failed to load profile data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProfileData();
  }, [language]);

  if (authLoading || loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/auth" replace />;
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-screen">
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  if (!profile) return null;

  return <ProfileView profile={profile} />;
};

export default ProfilePage;
