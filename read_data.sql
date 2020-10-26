\COPY users FROM 'mock_data/users_mock.csv' WITH DELIMITER ',' CSV HEADER;

\COPY petowners FROM 'mock_data/petowner_mock.csv' WITH DELIMITER ',' CSV HEADER;

\COPY ownedpets FROM 'mock_data/pet_owned.csv' WITH DELIMITER ',' CSV HEADER;

\COPY caretakers FROM 'mock_data/caretaker_mock.csv' WITH DELIMITER ',' CSV HEADER;

\COPY fulltime FROM 'mock_data/fulltime_mock.csv' WITH DELIMITER ',' CSV HEADER;

\COPY parttime FROM 'mock_data/parttime_mock.csv' WITH DELIMITER ',' CSV HEADER;

-- \COPY modeoftransport FROM 'mock_data/transport_mode.csv' WITH DELIMITER ',' CSV HEADER;

\COPY preferredtransport FROM 'mock_data/prefer_transport_mock.csv' WITH DELIMITER ',' CSV HEADER;

\COPY CaretakerAvailability FROM 'mock_data/availability.csv' WITH DELIMITER ',' CSV HEADER;

\COPY PartTimePriceList FROM 'mock_data/parttime_price.csv' WITH DELIMITER ',' CSV HEADER;

\COPY FullTimePriceList FROM 'mock_data/fulltime_price.csv' WITH DELIMITER ',' CSV HEADER;

\COPY bids FROM 'mock_data/bid.csv' WITH DELIMITER ',' CSV HEADER;
