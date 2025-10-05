import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import './index.css';
import 'primereact/resources/themes/lara-light-blue/theme.css';  
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';


const container = document.getElementById('root')!;
const root = createRoot(container);
root.render(<React.StrictMode><App /></React.StrictMode>);
