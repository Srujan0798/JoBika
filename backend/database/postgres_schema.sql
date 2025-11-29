-- JoBika Production PostgreSQL Schema
-- For deployment to Railway, Supabase, or any PostgreSQL instance

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users Table (Complete)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(15),
    full_name VARCHAR(255) NOT NULL,
    profile_picture_url TEXT,
    
    -- Location
    current_city VARCHAR(100),
    current_state VARCHAR(100),
    preferred_locations TEXT[],
    open_to_relocate BOOLEAN DEFAULT false,
    open_to_remote BOOLEAN DEFAULT true,
    
    -- Current employment
    current_company VARCHAR(255),
    current_title VARCHAR(255),
    current_ctc DECIMAL(12,2), -- In INR
    expected_ctc_min DECIMAL(12,2),
    expected_ctc_max DECIMAL(12,2),
    total_experience_months INTEGER DEFAULT 0,
    notice_period_days INTEGER DEFAULT 30,
    
    -- Preferences
    target_roles TEXT[],
    target_industries TEXT[],
    job_type_preferences TEXT[],
    company_size_preferences TEXT[],
    
    -- Subscription
    subscription_tier VARCHAR(50) DEFAULT 'free',
    subscription_expires_at TIMESTAMP,
    daily_credits INTEGER DEFAULT 5,
    credits_used_today INTEGER DEFAULT 0,
    credits_reset_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active_at TIMESTAMP,
    onboarding_completed BOOLEAN DEFAULT false,
    email_verified BOOLEAN DEFAULT false,
    phone_verified BOOLEAN DEFAULT false
);

-- Resumes
CREATE TABLE resumes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    is_primary BOOLEAN DEFAULT false,
    
    -- Content (JSONB for flexibility)
    personal_info JSONB,
    summary TEXT,
    experience JSONB,
    education JSONB,
    skills TEXT[],
    projects JSONB,
    certifications JSONB,
    
    -- Files
    original_file_url TEXT,
    generated_pdf_url TEXT,
    
    -- Scoring
    ats_score INTEGER,
    last_tailored_for_job_id UUID,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Jobs
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Basic Info
    title VARCHAR(255) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    job_type VARCHAR(50),
    work_mode VARCHAR(50),
    
    -- Details
    description TEXT,
    requirements TEXT,
    qualifications JSONB,
    
    -- Skills & Experience
    required_skills TEXT[],
    preferred_skills TEXT[],
    min_experience_months INTEGER,
    max_experience_months INTEGER,
    
    -- Compensation (INR)
    salary_min DECIMAL(12,2),
    salary_max DECIMAL(12,2),
    show_salary BOOLEAN DEFAULT false,
    
    -- Application
    apply_url TEXT,
    apply_email VARCHAR(255),
    application_deadline DATE,
    
    -- Source
    source_platform VARCHAR(50),
    source_url TEXT,
    source_job_id VARCHAR(255),
    
    -- Status
    status VARCHAR(20) DEFAULT 'active',
    is_verified BOOLEAN DEFAULT false,
    is_fake_probability DECIMAL(3,2),
    applicant_count INTEGER DEFAULT 0,
    
    -- Metadata
    posted_date TIMESTAMP,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for jobs
CREATE INDEX idx_jobs_title ON jobs(title);
CREATE INDEX idx_jobs_company ON jobs(company_name);
CREATE INDEX idx_jobs_location ON jobs(location);
CREATE INDEX idx_jobs_posted ON jobs(posted_date DESC);
CREATE INDEX idx_jobs_skills ON jobs USING gin(required_skills);
CREATE INDEX idx_jobs_search ON jobs USING gin(
    to_tsvector('english', title || ' ' || COALESCE(description, '') || ' ' || company_name)
);

-- Applications
CREATE TABLE applications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    job_id UUID REFERENCES jobs(id),
    
    -- External job (if not in our DB)
    external_job_title VARCHAR(255),
    external_company_name VARCHAR(255),
    external_job_url TEXT,
    
    -- Status
    status VARCHAR(50) NOT NULL DEFAULT 'applied',
    status_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Application details
    applied_via VARCHAR(50),
    resume_version_id UUID REFERENCES resumes(id),
    cover_letter TEXT,
    
    -- Tracking
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    viewed_at TIMESTAMP,
    response_received_at TIMESTAMP,
    interview_scheduled_at TIMESTAMP,
    
    -- Notes
    notes TEXT,
    next_followup_date DATE,
    tags TEXT[],
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_applications_user ON applications(user_id);
CREATE INDEX idx_applications_status ON applications(status);
CREATE INDEX idx_applications_date ON applications(applied_at DESC);

-- Application Events (Timeline)
CREATE TABLE application_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    application_id UUID REFERENCES applications(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL,
    old_status VARCHAR(50),
    new_status VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Saved Jobs
CREATE TABLE saved_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, job_id)
);

CREATE INDEX idx_saved_jobs_user ON saved_jobs(user_id);

-- Job Alerts
CREATE TABLE job_alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255),
    
    -- Filters
    keywords TEXT[],
    locations TEXT[],
    job_types TEXT[],
    experience_min INTEGER,
    experience_max INTEGER,
    salary_min DECIMAL(12,2),
    companies TEXT[],
    
    -- Settings
    frequency VARCHAR(20) DEFAULT 'daily',
    channels TEXT[] DEFAULT ARRAY['email'],
    is_active BOOLEAN DEFAULT true,
    last_sent_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chat Messages (Orion AI)
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    session_id UUID,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    context JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_chat_user_session ON chat_messages(user_id, session_id);
CREATE INDEX idx_chat_created ON chat_messages(created_at DESC);

-- Companies (for insights)
CREATE TABLE companies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE,
    
    -- Basic info
    description TEXT,
    industry VARCHAR(100),
    company_type VARCHAR(50),
    website_url TEXT,
    
    -- Ratings
    overall_rating DECIMAL(2,1),
    review_count INTEGER DEFAULT 0,
    
    -- Metadata
    logo_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Usage Tracking (for tier limits)
CREATE TABLE usage_tracking (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    action_type VARCHAR(50) NOT NULL, -- 'application', 'chat', 'resume_tailor', etc.
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    count INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, action_type, date)
);

CREATE INDEX idx_usage_user_date ON usage_tracking(user_id, date);

-- Update Triggers
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_jobs_updated_at BEFORE UPDATE ON jobs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_applications_updated_at BEFORE UPDATE ON applications
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_resumes_updated_at BEFORE UPDATE ON resumes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Sample Data (Optional - for testing)
INSERT INTO jobs (title, company_name, location, job_type, work_mode, description, required_skills, salary_min, salary_max, posted_date)
VALUES 
('Software Engineer', 'Google India', 'Bangalore', 'full_time', 'hybrid', 'Join our team to build amazing products', ARRAY['Python', 'Java', 'Kubernetes'], 2000000, 4500000, CURRENT_TIMESTAMP),
('Frontend Developer', 'Flipkart', 'Bangalore', 'full_time', 'onsite', 'Build user interfaces', ARRAY['React', 'JavaScript', 'CSS'], 1200000, 3000000, CURRENT_TIMESTAMP),
('Data Scientist', 'Amazon', 'Hyderabad', 'full_time', 'remote', 'Work with big data and ML', ARRAY['Python', 'ML', 'Statistics'], 1500000, 3500000, CURRENT_TIMESTAMP);

-- Grant permissions (if needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO jobika_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO jobika_user;
