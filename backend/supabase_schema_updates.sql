-- Schema updates for migrating mock data to PostgreSQL

-- 11. Salary Roles table
CREATE TABLE IF NOT EXISTS salary_roles (
    id SERIAL PRIMARY KEY,
    role_name TEXT UNIQUE NOT NULL,
    min_salary INTEGER,
    max_salary INTEGER,
    median_salary INTEGER,
    demand_level TEXT,
    growth_trend TEXT,
    competition_level TEXT,
    top_skills TEXT, -- JSON string of skills
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 12. Location Multipliers table
CREATE TABLE IF NOT EXISTS location_multipliers (
    id SERIAL PRIMARY KEY,
    location_name TEXT UNIQUE NOT NULL,
    multiplier FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 13. Interview Questions table
CREATE TABLE IF NOT EXISTS interview_questions (
    id SERIAL PRIMARY KEY,
    category TEXT NOT NULL, -- technical, behavioral, company, role_specific
    question_template TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 14. Interview Tips table
CREATE TABLE IF NOT EXISTS interview_tips (
    id SERIAL PRIMARY KEY,
    stage TEXT NOT NULL, -- preparation, during, after
    tip_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 15. Domain Skills table (for Resume Customizer)
CREATE TABLE IF NOT EXISTS domain_skills (
    id SERIAL PRIMARY KEY,
    domain_name TEXT UNIQUE NOT NULL, -- full_stack, backend, etc.
    skills_list TEXT NOT NULL, -- JSON string of skills
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
