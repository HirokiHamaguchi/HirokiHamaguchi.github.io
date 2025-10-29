import React from 'react';
import ReactDOM from 'react-dom/client';
import { ChakraProvider } from '@chakra-ui/react';
import App from './App';
import './i18n';

const rootElement = document.getElementById('hit-and-blow-root');
if (rootElement) {
    const root = ReactDOM.createRoot(rootElement);
    root.render(
        <React.StrictMode>
            <ChakraProvider>
                <App />
            </ChakraProvider>
        </React.StrictMode>
    );
}