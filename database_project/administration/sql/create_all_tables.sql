CREATE TABLE all_users (
    user_id SERIAL PRIMARY KEY,
    forename VARCHAR(255),
    surname VARCHAR(255),
    username VARCHAR(255),
    password VARCHAR(255),
    account_money BIGINT
);

CREATE TABLE swimming_pool(
    pool_id SERIAL PRIMARY KEY,
    number_of_lanes INT NOT NULL,
    opening_hour TIME NOT NULL,
    closing_hour TIME NOT NULL,
    working_days VARCHAR(255) NOT NULL
);

CREATE TABLE worker (
    worker_id SERIAL PRIMARY KEY,
    pool_id INT,
    salary INT,
    age INT,
    gender VARCHAR(100),
    phone_number VARCHAR(15),
    swim_proficiency VARCHAR(100),
    qualifications TEXT,
    FOREIGN KEY (worker_id) REFERENCES all_users(user_id),
    FOREIGN KEY (pool_id) REFERENCES swimming_pool(pool_id)
);

CREATE TABLE coach (
    coach_id SERIAL PRIMARY KEY,
    avg_rating FLOAT,
    coach_ranking INT,
    specialties TEXT,
    FOREIGN KEY (coach_id) REFERENCES worker(worker_id)
);

CREATE TABLE lifeguard (
    lifeguard_id SERIAL PRIMARY KEY,
    certifications TEXT,
    FOREIGN KEY (lifeguard_id) REFERENCES worker(worker_id)
);

CREATE TABLE administrator (
    administrator_id SERIAL PRIMARY KEY,
    number_of_reports INT,
    FOREIGN KEY (administrator_id) REFERENCES all_users(user_id)
);

CREATE TABLE lane(
    lane_id SERIAL PRIMARY KEY,
    pool_id INT,
    lane_number INT,
    lifeguard_id INT,
    FOREIGN KEY (pool_id) REFERENCES swimming_pool(pool_id),
    FOREIGN KEY (lifeguard_id) REFERENCES lifeguard(lifeguard_id)
);

CREATE TABLE swimmer (
    swimmer_id SERIAL PRIMARY KEY,
    phone_number VARCHAR(15),
    age INT,
    gender VARCHAR(100),
    swimming_proficiency VARCHAR(100),
    number_of_booked_slots INT,
    total_courses_enrolled INT,
    total_courses_terminated INT,
    FOREIGN KEY (swimmer_id) REFERENCES all_users(user_id)
);

CREATE TABLE member_swimmer(
    swimmer_id SERIAL PRIMARY KEY,
    points INT,
    monthly_payment_amount INT,
    personal_coach_id INT,
    number_of_personal_training_hours INT,
    ranking INT,
    number_of_items_purchased INT,
    FOREIGN KEY (swimmer_id) REFERENCES swimmer(swimmer_id),
    FOREIGN KEY (personal_coach_id) REFERENCES coach(coach_id)
);

CREATE TABLE nonmember_swimmer (
    swimmer_id SERIAL PRIMARY KEY,
    registration_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (swimmer_id) REFERENCES swimmer(swimmer_id)
);

CREATE TABLE report (
    report_id SERIAL PRIMARY KEY,
    admin_id INT,
    report_content_info VARCHAR(255),
    report_content TEXT,
    report_file BYTEA,
    FOREIGN KEY (admin_id) REFERENCES administrator(administrator_id)
);

CREATE TABLE course(
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(255) NOT NULL,
    course_image BYTEA,
    coach_id INT NOT NULL,
    course_description TEXT,
    restrictions VARCHAR(255),
    deadline DATE,
    pool_id INT NOT NULL,
    lane_id INT NOT NULL,
    price INT NOT NULL,
    FOREIGN KEY (coach_id) REFERENCES coach(coach_id),
    FOREIGN KEY (pool_id) REFERENCES swimming_pool(pool_id),
    FOREIGN KEY (lane_id) REFERENCES lane(lane_id)
);

CREATE TABLE course_schedule(
    course_schedule_id SERIAL PRIMARY KEY,
    course_id INT,
    swimmer_id INT,
    coach_id INT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    day VARCHAR(255),
    FOREIGN KEY (swimmer_id) REFERENCES swimmer(swimmer_id),
    FOREIGN KEY (coach_id) REFERENCES coach(coach_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE personal_training(
    training_id SERIAL PRIMARY KEY,
    FOREIGN KEY (training_id) REFERENCES course(course_id)
);

CREATE TABLE swimming_lesson(
    lesson_id SERIAL PRIMARY KEY,
    capacity INT NOT NULL,
    is_full BOOLEAN NOT NULL,
    FOREIGN KEY (lesson_id) REFERENCES course(course_id)
);

CREATE TABLE time_slot(
    time_slot_id SERIAL PRIMARY KEY,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    lane_id INT NOT NULL,
    is_booked BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (lane_id) REFERENCES lane(lane_id)
);

CREATE TABLE cafe(
    cafe_id SERIAL PRIMARY KEY,
    number_of_items INT,
    pool_id INT,
    FOREIGN KEY (pool_id) REFERENCES swimming_pool(pool_id)
);

CREATE TABLE cafe_item(
    cafe_item_id SERIAL PRIMARY KEY,
    cafe_id INT NOT NULL,
    item_image BYTEA,
    item_description VARCHAR(255),
    item_count INT,
    FOREIGN KEY (cafe_id) REFERENCES cafe(cafe_id)
);

CREATE TABLE rating(
    rating_id SERIAL PRIMARY KEY,
    swimmer_id INT NOT NULL, 
    coach_id INT NOT NULL,
    course_id INT NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (swimmer_id) REFERENCES swimmer(swimmer_id),
    FOREIGN KEY (coach_id) REFERENCES coach(coach_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE comment(
    comment_id SERIAL PRIMARY KEY,
    swimmer_id INT NOT NULL, 
    coach_id INT NOT NULL,
    course_id INT NOT NULL,
    comment VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (swimmer_id) REFERENCES swimmer(swimmer_id),
    FOREIGN KEY (coach_id) REFERENCES coach(coach_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE cart(
    cart_id SERIAL PRIMARY KEY,
    purchaser_id INT NOT NULL,
    course_id INT,
    cafe_item_id INT,
    cafe_id INT,
    FOREIGN KEY (purchaser_id) REFERENCES swimmer(swimmer_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id),
    FOREIGN KEY (cafe_item_id) REFERENCES cafe_item(cafe_item_id),
    FOREIGN KEY (cafe_id) REFERENCES cafe(cafe_id)
);

