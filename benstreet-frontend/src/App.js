import React from 'react';
import ReactDOM from 'react-dom/client';
import Trader from './components/Trader';
import Summary from './components/Summary';
import Activity from './components/Activity';
import AppInfo from './components/AppInfo';

const App = () => {
    return (
        <div className='App'>
            <span className="nav">
                <span className="nav-title">
                <h1>Ben Street</h1>
                <h3><i>"Invest Ben's Money"</i></h3>
                </span>
                
                
                <AppInfo/>
            </span>
            <Trader />
            <div className='summarycontainer'>
                <Summary />
                <Activity />
            </div>
        </div>
    )
}

export default App