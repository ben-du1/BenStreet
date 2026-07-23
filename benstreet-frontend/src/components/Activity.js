import React from 'react';
import ReactDOM from 'react-dom/client';
import {useState, useEffect} from 'react'

function Activity() {
    const [activity, setActivity] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch("http://localhost:3001/api/activity")
            .then((res) => {
                if (!res.ok) {
                    throw new Error("Failed to fetch activity");
                }
                return res.json();
            })
            .then((data) => {
                setActivity(data);
            })
            .catch((err) => {
                setError(err.message);
            });
    }, []);

    if (error) {
        return (
            <div className="activity-error">
                {error}
            </div>
        );
    }

    return (
        <div className="activity-container">
            {activity.map((trade) => {

                const isBuy =
                    trade.side === "B"

                return (
                    <div
                        key={trade.id}
                        className={`activity-item ${
                            isBuy ? "buy" : "sell"
                        }`}
                    >
                        <div className="activity-message">

                            <span className="action">
                                {isBuy ? "BUY" : "SELL"}
                            </span>

                            <span>
                                {" "}
                                {trade.shares} shares of{" "}
                            </span>

                            <span className="ticker">
                                {trade.ticker}
                            </span>

                            <span>
                                {" "}@
                                {" "}
                            </span>

                            <span className="price">
                                ${Number(trade.price).toFixed(2)}
                            </span>

                        </div>

                        <div className="activity-meta">
                            {trade.status}
                            {" • "}
                            {new Date(trade.timestamp).toLocaleString()}
                        </div>
                    </div>
                );
            })}
        </div>
    );
}

export default Activity;