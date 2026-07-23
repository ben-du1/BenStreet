import React from "react";
import {
    PieChart,
    Pie,
    Cell,
    Tooltip,
    Legend,
    ResponsiveContainer
} from "recharts";

const COLORS = [
    "#22c55e",
    "#3b82f6",
    "#f59e0b",
    "#ef4444",
    "#8b5cf6",
    "#14b8a6",
    "#f97316",
    "#ec4899",
    "#84cc16",
    "#6366f1"
];

function PortfolioPie({ portfolio }) {

    if (!portfolio) {
        return null;
    }

    const data = [
    ...portfolio.positions
        .filter(position =>
            position.ticker &&
            Number(position.marketValue) > 0
        )
        .map(position => ({
            name: position.ticker,
            value: Number(position.marketValue)
        })),
    ...(Number(portfolio.cash) > 0
        ? [{
            name: "Cash",
            value: Number(portfolio.cash)
        }]
        : [])
];

    return (
        <div className="portfolio-pie">

            <h2>Portfolio Allocation</h2>

            <ResponsiveContainer
                width="100%"
                height={300}
            >
                <PieChart>

                    <Pie
                        data={data}
                        dataKey="value"
                        nameKey="name"
                        outerRadius={100}
                        label={({ name, percent }) =>
                            `${name} ${(percent * 100).toFixed(1)}%`
                        }
                    >
                        {data.map((entry, index) => (
                            <Cell
                                key={entry.name}
                                fill={COLORS[index % COLORS.length]}
                            />
                        ))}
                    </Pie>

                    <Tooltip
                        formatter={(value) =>
                            `$${Number(value).toFixed(2)}`
                        }
                    />

                    <Legend />

                </PieChart>
            </ResponsiveContainer>

        </div>
    );
}

export default PortfolioPie;