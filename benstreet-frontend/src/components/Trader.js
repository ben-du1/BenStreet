import { useState } from "react";
import { SERVER_URL_BASE } from '../lib/config';

const Trader = () => {

    const [ticker, setTicker] = useState("");
    const [loading, setLoading] = useState(false);

    const trade = async (side) => {

        const symbol = ticker.trim().toUpperCase();

        if (!symbol) {
            alert("Please enter a ticker.");
            return;
        }

        setLoading(true);

        try {

            const response = await fetch(
                `${SERVER_URL_BASE}/api/${side}?ticker=${symbol}`,
                {
                    method: "POST",
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.detail || "Trade failed."
                );
            }

            alert(`${side.toUpperCase()} submitted successfully.`);

        } catch (err) {

            alert(err.message);

        } finally {

            setLoading(false);

        }
    };

    return (
        <div className="trader">

            <input
                type="text"
                placeholder="Ticker (e.g. AAPL)"
                value={ticker}
                onChange={(e) =>
                    setTicker(e.target.value.toUpperCase())
                }
                maxLength={5}
            />

            <button
                className="buy-button"
                disabled={loading}
                onClick={() => trade("buy")}
            >
                Buy $1
            </button>

            <button
                className="sell-button"
                disabled={loading}
                onClick={() => trade("sell")}
            >
                Sell $1
            </button>

        </div>
    );
};

export default Trader;