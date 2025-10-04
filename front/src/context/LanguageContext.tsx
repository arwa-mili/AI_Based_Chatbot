import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import enTranslations from '../locales/en.json';
import arTranslations from '../locales/ar.json';

i18n.use(initReactI18next).init({
  resources: {
    en: { translation: enTranslations },
    ar: { translation: arTranslations },
  },
  lng: 'en',
  fallbackLng: 'en',
  interpolation: { escapeValue: false },
});

interface LanguageContextType {
  language: 'en' | 'ar';
  toggleLanguage: () => void;
  setLanguage: (lang: 'en' | 'ar') => void;
  t: (key: string) => string;
  isRTL: boolean;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export const LanguageProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [language, setLanguageState] = useState<'en' | 'ar'>('en');

  useEffect(() => {
    const savedLang = localStorage.getItem('language') as 'en' | 'ar';
    if (savedLang) {
      setLanguageState(savedLang);
      i18n.changeLanguage(savedLang);
    }
  }, []);

  const setLanguage = (lang: 'en' | 'ar') => {
    setLanguageState(lang);
    i18n.changeLanguage(lang);
    localStorage.setItem('language', lang);
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
    document.documentElement.lang = lang;
  };

  const toggleLanguage = () => {
    const newLang = language === 'en' ? 'ar' : 'en';
    setLanguage(newLang);
  };

  const t = (key: string): string => {
    return i18n.t(key);
  };

  return (
    <LanguageContext.Provider
      value={{
        language,
        toggleLanguage,
        setLanguage,
        t,
        isRTL: language === 'ar',
      }}
    >
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) throw new Error('useLanguage must be used within LanguageProvider');
  return context;
};