CREATE TABLE IF NOT EXISTS hangman_users (
            id integer PRIMARY KEY AUTOINCREMENT,
            name text,
            surname text,
            email TEXT NOT NULL UNIQUE,
            pasword text,
            time integer NOT NULL
            );

CREATE TABLE IF NOT EXISTS hangman_dictionary (
            id integer PRIMARY KEY AUTOINCREMENT,
            words TEXT NOT NULL UNIQUE
            );

CREATE TABLE IF NOT EXISTS game_sassion (
            id integer PRIMARY KEY AUTOINCREMENT,
            user_id integer,
            random_words TEXT NOT NULL,
            word_len integer,
            guess_letter_1 text,
            guess_letter_1_result,
            guess_letter_2 text,
            guess_letter_2_result,
            guess_letter_3 text,
            guess_letter_3_result,
            guess_letter_4 text,
            guess_letter_4_result,
            guess_letter_5 text,
            guess_letter_5_result,
            guess_letter_6 text,
            guess_letter_6_result,
            guess_letter_7 text,
            guess_letter_7_result,
            guess_letter_8 text,
            guess_letter_8_result,
            guess_letter_9 text,
            guess_letter_9_result,
            guess_letter_10 text,
            guess_letter_10_result,
            game_result,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
            );

