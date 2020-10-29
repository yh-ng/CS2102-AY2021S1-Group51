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

INSERT INTO CareTakerSalary VALUES (2019, 6, 'ckitleeg', 35, 2500, 2500);

CREATE OR REPLACE FUNCTION
update_salary() RETURNS trigger AS $$
DECLARE end_of_month date := (SELECT(date_trunc('month', NEW.start_date::date) + interval '1 month' - interval '1 day')::date);
DECLARE start_of_end_date_month date;
BEGIN
IF NEW.end_date > end_of_month THEN
start_of_end_date_month := (SELECT date_trunc('MONTH', NEW.end_date)::DATE);

UPDATE CareTakerSalary 
SET earnings = earnings + ((NEW.end_date - start_of_end_date_month + 1) * NEW.price), petdays = petdays + (NEW.end_date - start_of_end_date_month + 1)
WHERE
username = NEW.ct_username AND 
year = (SELECT date_part('year', start_of_end_date_month)) AND
month = (SELECT date_part('month', start_of_end_date_month));

NEW.end_date := end_of_month;
END IF;
UPDATE CareTakerSalary 
SET earnings = earnings + ((NEW.end_date - NEW.start_date + 1) * NEW.price), petdays = petdays + (NEW.end_date - NEW.start_date + 1)
WHERE
username = NEW.ct_username AND 
year = (SELECT date_part('year', NEW.start_date)) AND
month = (SELECT date_part('month', NEW.start_date)); 
RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER update_ct_salary
AFTER INSERT
ON "bids"
FOR EACH ROW
EXECUTE PROCEDURE update_salary();

\COPY bids FROM 'mock_data/bid.csv' WITH DELIMITER ',' CSV HEADER;
