import React from 'react';
import ReactDOM from 'react-dom/client';
import PortfolioPie from './PortfolioPie';
import {useEffect,useState} from 'react'

function Summary() {

    const [portfolio, setPortfolio] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {

        async function fetchPortfolio() {

            try {

                const response = await fetch(
                    "http://localhost:3001/api/portfolio"
                );

                if (!response.ok) {
                    throw new Error("Failed to fetch portfolio");
                }

                const data = await response.json();
                console.log(data);

                // Normalize the data for the chart
                setPortfolio({
                    cash: Number(data.cash),
                    positions: data.positions.map(position => ({
                        ticker: position.description,
                        marketValue: Number(position.marketValue)
                    }))
                });

            } catch (err) {

                setError(err.message);

            } finally {

                setLoading(false);

            }
        }

        fetchPortfolio();

    }, []);

    if (loading) {
        return <div>Loading portfolio...</div>;
    }

    if (error) {
        return <div>{error}</div>;
    }

    return (
        <div className="portfolio-overview">

        <PortfolioPie portfolio={portfolio} />

        <div className="holdings">

            <h2>Current Holdings</h2>

            <div className="holding cash">
                <span>Cash</span>
                <span>${portfolio.cash.toFixed(2)}</span>
            </div>

            {portfolio.positions.map(position => (
                <div
                    key={position.ticker}
                    className="holding"
                >
                    <span>{position.ticker}</span>

                    <span>
                        ${position.marketValue.toFixed(2)}
                    </span>
                </div>
            ))}

        </div>

    </div>
    
    )
}

export default Summary;