CREATE DATABASE moboodb;

\c moboodb;

DROP TABLE IF EXISTS predict_result;
CREATE TABLE predict_result (
  id serial NOT NULL PRIMARY KEY,
  file_name varchar NOT NULL,
  pred_result varchar NOT NULL,
  prob_result jsonb NOT NULL,
  created_at timestamp without time zone NOT NULL
);

CREATE SEQUENCE predict_result_id_seq START 1;