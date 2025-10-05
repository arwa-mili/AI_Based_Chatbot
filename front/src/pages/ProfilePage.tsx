import React, { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { ProfileView } from '../components/profile/ProfileView';
import { GetProfile, GetLastSummaryResponse } from '../types/profile.types';
import { getProfileInfo, getUserSummary } from '../services/profileService';

const ProfilePage: React.FC = () => {
  const { isAuthenticated, isLoading: authLoading } = useAuth();
  const [profile, setProfile] = useState<GetProfile | null>(null);
  const [summary, setSummary] = useState<GetLastSummaryResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadProfileData = async () => {
      try {
        const [profileRes, summaryRes] = await Promise.all([
          getProfileInfo(),
          getUserSummary(),
        ]);

        setProfile(profileRes.data);
        setSummary(summaryRes.data);
      } catch (err) {
        setError('Failed to load profile data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    loadProfileData();
  }, []);

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

  return <ProfileView profile={profile} summary={summary} />;
};

export default ProfilePage;
