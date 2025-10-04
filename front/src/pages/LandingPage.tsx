import React from 'react';
import { Hero } from '../components/landing/Hero';
import { Features } from '../components/landing/Features';
import { About } from '../components/landing/About';

export const LandingPage: React.FC = () => {
  return (
    <div>
      <Hero />
      <Features />
      <About />
    </div>
  );
};