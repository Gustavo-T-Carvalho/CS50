-- Keep a log of any SQL queries you execute as you solve the mystery.

SELECT * FROM crime_scene_reports WHERE description LIKE "%duck%";

| 295 | 2023 | 7     | 28  | Humphrey Street | Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery. |

SELECT * FROM interviews WHERE year = 2023 AND month = 7 and day = 28;
| 161 | Ruth    | 2023 | 7     | 28  | Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.                                                          |
| 162 | Eugene  | 2023 | 7     | 28  | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.                                                                                                 |
| 163 | Raymond | 2023 | 7     | 28  | As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket. |

SELECT * FROM bakery_security_logs WHERE year = 2023 AND month = 7 and day = 28;
| 260 | 2023 | 7     | 28  | 10   | 16     | exit     | 5P2BI95       |
| 261 | 2023 | 7     | 28  | 10   | 18     | exit     | 94KL13X       |
| 262 | 2023 | 7     | 28  | 10   | 18     | exit     | 6P58WS2       |
| 263 | 2023 | 7     | 28  | 10   | 19     | exit     | 4328GD8       |
| 264 | 2023 | 7     | 28  | 10   | 20     | exit     | G412CB7       |
| 265 | 2023 | 7     | 28  | 10   | 21     | exit     | L93JTIZ       |
| 266 | 2023 | 7     | 28  | 10   | 23     | exit     | 322W7JE       |
| 267 | 2023 | 7     | 28  | 10   | 23     | exit     | 0NTHK55

SELECT * FROM atm_transactions WHERE year = 2023 AND month = 7 AND day = 28 AND transaction_type = "withdraw" AND atm_location = "Leggett Street";
+-----+----------------+------+-------+-----+----------------+------------------+--------+
| id  | account_number | year | month | day |  atm_location  | transaction_type | amount |
+-----+----------------+------+-------+-----+----------------+------------------+--------+
| 246 | 28500762       | 2023 | 7     | 28  | Leggett Street | withdraw         | 48     |
| 264 | 28296815       | 2023 | 7     | 28  | Leggett Street | withdraw         | 20     |
| 266 | 76054385       | 2023 | 7     | 28  | Leggett Street | withdraw         | 60     |
| 267 | 49610011       | 2023 | 7     | 28  | Leggett Street | withdraw         | 50     |
| 269 | 16153065       | 2023 | 7     | 28  | Leggett Street | withdraw         | 80     |
| 288 | 25506511       | 2023 | 7     | 28  | Leggett Street | withdraw         | 20     |
| 313 | 81061156       | 2023 | 7     | 28  | Leggett Street | withdraw         | 30     |
| 336 | 26013199       | 2023 | 7     | 28  | Leggett Street | withdraw         | 35     |
+-----+----------------+------+-------+-----+----------------+------------------+--------+

SELECT * FROM people WHERE license_plate IN( SELECT license_plate FROM bakery_security_logs WHERE year = 2023 AND month = 7 and day = 28 AND hour = 10 AND minute > 15 AND minute < 25);
+--------+---------+----------------+-----------------+---------------+
|   id   |  name   |  phone_number  | passport_number | license_plate |
+--------+---------+----------------+-----------------+---------------+
| 221103 | Vanessa | (725) 555-4692 | 2963008352      | 5P2BI95       |
| 243696 | Barry   | (301) 555-4174 | 7526138472      | 6P58WS2       |
| 396669 | Iman    | (829) 555-5269 | 7049073643      | L93JTIZ       |
| 398010 | Sofia   | (130) 555-0289 | 1695452385      | G412CB7       |
| 467400 | Luca    | (389) 555-5198 | 8496433585      | 4328GD8       |
| 514354 | Diana   | (770) 555-1861 | 3592750733      | 322W7JE       |
| 560886 | Kelsey  | (499) 555-9472 | 8294398571      | 0NTHK55       |
| 686048 | Bruce   | (367) 555-5533 | 5773159633      | 94KL13X       |
+--------+---------+----------------+-----------------+---------------+

SELECT id,name FROM people WHERE id IN(
    SELECT person_id FROM bank_accounts WHERE account_number IN(
        SELECT account_number FROM atm_transactions WHERE year = 2023 AND month = 7 AND day = 28 AND transaction_type = "withdraw" AND atm_location = "Leggett Street")
);
+--------+---------+
|   id   |  name   |
+--------+---------+
| 395717 | Kenny   |
| 396669 | Iman    |
| 438727 | Benista |
| 449774 | Taylor  |
| 458378 | Brooke  |
| 467400 | Luca    |
| 514354 | Diana   |
| 686048 | Bruce   |
+--------+---------+

Suspects:
 396669 | Iman
 467400 | Luca
 514354 | Diana
 686048 | Bruce


SELECT * FROM flights WHERE year = 2023 AND month = 7 AND day = 29 AND origin_airport_id = (SELECT id FROM ai
rports WHERE city = "Fiftyville") ORDER BY hour ASC, minute ASC LIMIT 1;
+----+-------------------+------------------------+------+-------+-----+------+--------+
| id | origin_airport_id | destination_airport_id | year | month | day | hour | minute |
+----+-------------------+------------------------+------+-------+-----+------+--------+
| 36 | 8                 | 4                      | 2023 | 7     | 29  | 8    | 20     |
+----+-------------------+------------------------+------+-------+-----+------+--------+


- GET SUSPECTS ids based on merging the search result of license_plates and atm_transactions
SELECT licensePlateQuery.id FROM
(SELECT * FROM people WHERE license_plate IN( SELECT license_plate FROM bakery_security_logs WHERE year = 2023 AND month = 7 and day = 28 AND hour = 10 AND minute > 15 AND minute < 25)) licensePlateQuery
JOIN
(SELECT id,name FROM people WHERE id IN(
    SELECT person_id FROM bank_accounts WHERE account_number IN(
        SELECT account_number FROM atm_transactions WHERE year = 2023 AND month = 7 AND day = 28 AND transaction_type = "withdraw" AND atm_location = "Leggett Street")
)) bankAccountsQuery
ON bankAccountsQuery.id = licensePlateQuery.id;

SELECT * from PASSENGERS WHERE flight_id = 36 AND passport_number IN (
    SELECT passport_number FROM people WHERE id IN(
        SELECT licensePlateQuery.id FROM
(SELECT * FROM people WHERE license_plate IN( SELECT license_plate FROM bakery_security_logs WHERE year = 2023 AND month = 7 and day = 28 AND hour = 10 AND minute > 15 AND minute < 25)) licensePlateQuery
JOIN
(SELECT id,name FROM people WHERE id IN(
    SELECT person_id FROM bank_accounts WHERE account_number IN(
        SELECT account_number FROM atm_transactions WHERE year = 2023 AND month = 7 AND day = 28 AND transaction_type = "withdraw" AND atm_location = "Leggett Street")
)) bankAccountsQuery
ON bankAccountsQuery.id = licensePlateQuery.id
    )
);

+-----------+-----------------+------+
| flight_id | passport_number | seat |
+-----------+-----------------+------+
| 36        | 5773159633      | 4A   |
| 36        | 8496433585      | 7B   |
+-----------+-----------------+------+

SELECT * FROM people WHERE passport_number = "5773159633" OR passport_number = "8496433585"
+--------+-------+----------------+-----------------+---------------+
|   id   | name  |  phone_number  | passport_number | license_plate |
+--------+-------+----------------+-----------------+---------------+
| 467400 | Luca  | (389) 555-5198 | 8496433585      | 4328GD8       |
| 686048 | Bruce | (367) 555-5533 | 5773159633      | 94KL13X       |
+--------+-------+----------------+-----------------+---------------+

 SELECT city FROM airports WHERE id = (
    SELECT destination_airport_id FROM flights where id = 36
 );
+---------------+
|     city      |
+---------------+
| New York City |
+---------------+

SELECT * FROM phone_calls WHERE year = 2023 AND month = 7 AND day = 28 AND caller IN(
    SELECT phone_number FROM people WHERE passport_number = "5773159633" OR passport_number = "8496433585"
);
+-----+----------------+----------------+------+-------+-----+----------+
| id  |     caller     |    receiver    | year | month | day | duration |
+-----+----------------+----------------+------+-------+-----+----------+
| 233 | (367) 555-5533 | (375) 555-8161 | 2023 | 7     | 28  | 45       |
| 236 | (367) 555-5533 | (344) 555-9601 | 2023 | 7     | 28  | 120      |
| 245 | (367) 555-5533 | (022) 555-4052 | 2023 | 7     | 28  | 241      |
| 285 | (367) 555-5533 | (704) 555-5790 | 2023 | 7     | 28  | 75       |
+-----+----------------+----------------+------+-------+-----+----------+


SELECT * FROM people WHERE phone_number IN(
    SELECT receiver FROM phone_calls WHERE year = 2023 AND month = 7 AND day = 28 AND caller IN(
        SELECT phone_number FROM people WHERE passport_number = "5773159633" OR passport_number = "8496433585"
));
+--------+---------+----------------+-----------------+---------------+
|   id   |  name   |  phone_number  | passport_number | license_plate |
+--------+---------+----------------+-----------------+---------------+
| 315221 | Gregory | (022) 555-4052 | 3355598951      | V4C670D       |
| 652398 | Carl    | (704) 555-5790 | 7771405611      | 81MZ921       |
| 864400 | Robin   | (375) 555-8161 | NULL            | 4V16VO0       |
| 985497 | Deborah | (344) 555-9601 | 8714200946      | 10I5658       |
+--------+---------+----------------+-----------------+---------------+

SELECT * FROM people WHERE id IN(
SELECT person_id from bank_accounts WHERE person_id IN(
     SELECT id FROM people WHERE phone_number IN(
        SELECT receiver FROM phone_calls WHERE year = 2023 AND month = 7 AND day = 28 AND caller IN(
            SELECT phone_number FROM people WHERE passport_number = "5773159633" OR passport_number = "8496433585"
    ))
));

+--------+-------+----------------+-----------------+---------------+
|   id   | name  |  phone_number  | passport_number | license_plate |
+--------+-------+----------------+-----------------+---------------+
| 864400 | Robin | (375) 555-8161 | NULL            | 4V16VO0       |
+--------+-------+----------------+-----------------+---------------+

