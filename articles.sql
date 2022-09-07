

DROP TABLE IF EXISTS JUMIA_MAROC;
CREATE TABLE JUMIA_MAROC(
    id_jum_mar  SERIAL PRIMARY KEY,
    images_jum_mar VARCHAR (255) NOT NULL,
    details_jum_mar VARCHAR (255) NOT NULL,
    prices_jum_mar FLOAT
);

DROP TABLE IF EXISTS JUMIA_CI;
CREATE TABLE JUMIA_CI(
    id_jum_ci SERIAL PRIMARY KEY,
    images_jum_ci VARCHAR (255),
    details_jum_ci VARCHAR (255),
    prices_jum_ci FLOAT
);
DROP TABLE IF EXISTS JUMIA;
CREATE TABLE JUMIA(
    id_jumia SERIAL PRIMARY KEY,
    images_jumia VARCHAR (255),
    details_jumia VARCHAR (255),
    prices_in_CFA_jumia FLOAT
);
