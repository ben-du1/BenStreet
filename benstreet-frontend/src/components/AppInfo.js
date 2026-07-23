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
                        This application allows users to interact with
                        a live investment portfolio through a web interface.
                        Users can place $1 buy and sell orders, view current
                        holdings, monitor portfolio allocation, and track
                        executed trades.
                    </p>

                    <p>
                        Trades are routed through Interactive Brokers and
                        portfolio data is updated dynamically from the
                        brokerage account.
                    </p>

                </div>
            )}

        </div>
    );
}

export default AppInfo;