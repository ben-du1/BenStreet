import React, { useState } from "react";

function AppInfo() {

    const [showInfo, setShowInfo] = useState(false);

    return (
        <div className="app-info-wrapper">

            <button
                className="info-button"
                onMouseEnter={() => setShowInfo(true)}
                onMouseLeave={() => setShowInfo(false)}
            >
                ?
            </button>


            {showInfo && (
                <div className="app-info-popup">

                    <h3>About This App</h3>

                    <p>
                        Yes, this is actually my money. That's why you can only trade in dollar amounts. Note that buy orders cannot be placed outside of regular market hours.
                    </p>
                    <br />
                    <p>
                        Trades are routed through my Interactive Brokers account and
                        portfolio data is updated dynamically from the
                        brokerage account.
                    </p>

                </div>
            )}

        </div>
    );
}

export default AppInfo;