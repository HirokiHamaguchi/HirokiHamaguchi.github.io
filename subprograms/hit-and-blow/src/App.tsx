import React from 'react';
import Game from './components/Game';

const App: React.FC = () => {
    React.useEffect(() => {
        console.log("Hi there! The following are hints for this game:");
    }, []);
    return <Game />;
};

export default App;