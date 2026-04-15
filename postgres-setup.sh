sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'password';"
sudo -u postgres psql -d postgres <<EOF
CREATE TABLE mqtt_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITHOUT TIME ZONE,
    topic TEXT,
    message TEXT
);
EOF
