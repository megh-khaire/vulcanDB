-- Link - https://data.ny.gov/Government-Finance/Lottery-Powerball-Winning-Numbers-Beginning-2010/d6yy-54nr/about_data
CREATE TABLE PowerballWinningNumbers (
    draw_date DATE PRIMARY KEY,
    winning_numbers VARCHAR(255) NOT NULL,
    multiplier INT CHECK (multiplier >= 1)
);