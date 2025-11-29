const { z } = require('zod');

/**
 * Complete Validation Schemas for All Endpoints
 * Indian market specific validations
 */

// Alert Schema
const alertSchema = z.object({
    name: z.string().min(1).max(255),
    keywords: z.array(z.string()).optional(),
    locations: z.array(z.string()).optional(),
    jobTypes: z.array(z.string()).optional(),
    experienceMin: z.number().int().min(0).optional(),
    experienceMax: z.number().int().min(0).optional(),
    salaryMin: z.number().min(0).optional(),
    companies: z.array(z.string()).optional(),
    frequency: z.enum(['instant', 'daily', 'weekly']).optional(),
    channels: z.array(z.enum(['email', 'push', 'sms', 'whatsapp'])).optional()
});

// Profile Update Schema
const profileUpdateSchema = z.object({
    fullName: z.string().min(1).max(255).optional(),
    phone: z.string().regex(/^[6-9]\d{9}$/, 'Invalid Indian mobile number').optional(),
    currentCity: z.string().max(100).optional(),
    currentState: z.string().max(100).optional(),
    preferredLocations: z.array(z.string()).optional(),
    openToRelocate: z.boolean().optional(),
    openToRemote: z.boolean().optional(),
    currentCompany: z.string().max(255).optional(),
    currentTitle: z.string().max(255).optional(),
    currentCTC: z.number().min(0).optional(),
    expectedCTCMin: z.number().min(0).optional(),
    expectedCTCMax: z.number().min(0).optional(),
    totalExperienceMonths: z.number().int().min(0).optional(),
    noticePeriodDays: z.enum([0, 15, 30, 60, 90]).optional(),
    targetRoles: z.array(z.string()).optional(),
    targetIndustries: z.array(z.string()).optional()
});

// Application Status Update
const applicationStatusSchema = z.object({
    status: z.enum([
        'saved',
        'applied',
        'viewed',
        'phone_screen',
        'interview_scheduled',
        'interview_completed',
        'offer',
        'accepted',
        'rejected',
        'withdrawn'
    ]),
    notes: z.string().optional()
});

// Application Notes
const applicationNotesSchema = z.object({
    notes: z.string().max(2000),
    nextFollowupDate: z.string().datetime().optional()
});

// Saved Job Schema
const savedJobSchema = z.object({
    jobId: z.string().uuid(),
    notes: z.string().max(500).optional()
});

// Job Search Advanced
const jobSearchAdvancedSchema = z.object({
    keywords: z.string().optional(),
    locations: z.array(z.string()).optional(),
    experienceMin: z.number().int().min(0).max(50).optional(),
    experienceMax: z.number().int().min(0).max(50).optional(),
    salaryMin: z.number().min(0).optional(),
    salaryMax: z.number().min(0).optional(),
    jobTypes: z.array(z.enum(['full_time', 'part_time', 'contract', 'internship', 'freelance'])).optional(),
    workModes: z.array(z.enum(['remote', 'hybrid', 'onsite'])).optional(),
    companyTypes: z.array(z.enum(['mnc', 'indian_it_services', 'product', 'startup', 'psu', 'government'])).optional(),
    postedWithinDays: z.number().int().min(1).max(365).optional(),
    sortBy: z.enum(['relevance', 'date', 'salary']).optional(),
    page: z.number().int().min(1).optional(),
    perPage: z.number().int().min(1).max(100).optional()
});

// Education Schema
const educationSchema = z.object({
    institution: z.string().min(1).max(255),
    degree: z.string().max(100),
    fieldOfStudy: z.string().max(100).optional(),
    startDate: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
    endDate: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).optional(),
    gradeType: z.enum(['percentage', 'cgpa_10', 'cgpa_4']).optional(),
    gradeValue: z.number().min(0).max(100).optional(),
    isCurrent: z.boolean().optional()
});

// Experience Schema
const experienceSchema = z.object({
    company: z.string().min(1).max(255),
    title: z.string().min(1).max(255),
    location: z.string().max(255).optional(),
    startDate: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
    endDate: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).optional(),
    isCurrent: z.boolean().optional(),
    description: z.string().max(2000).optional(),
    skillsUsed: z.array(z.string()).optional(),
    achievements: z.array(z.string()).optional()
});

// Skills Schema
const skillsSchema = z.object({
    skillName: z.string().min(1).max(100),
    proficiencyLevel: z.enum(['beginner', 'intermediate', 'advanced', 'expert']).optional(),
    yearsOfExperience: z.number().min(0).max(50).optional(),
    isPrimary: z.boolean().optional()
});

// Company Review Schema
const companyReviewSchema = z.object({
    companyId: z.string().uuid(),
    rating: z.number().min(1).max(5),
    title: z.string().min(1).max(200),
    pros: z.string().min(1).max(1000),
    cons: z.string().min(1).max(1000),
    advice: z.string().max(1000).optional(),
    isCurrentEmployee: z.boolean(),
    jobTitle: z.string().max(100),
    department: z.string().max(100).optional()
});

// Insider Connection Request
const insiderConnectionSchema = z.object({
    companyId: z.string().uuid(),
    connectionName: z.string().min(1).max(255),
    connectionTitle: z.string().max(255).optional(),
    linkedinUrl: z.string().url().optional(),
    email: z.string().email().optional(),
    relationshipType: z.enum(['alumni', 'ex_colleague', 'mutual_connection', 'referral']),
    commonGround: z.string().max(500).optional(),
    notes: z.string().max(1000).optional()
});

// Agent Preferences
const agentPreferencesSchema = z.object({
    mode: z.enum(['supervised', 'autonomous']),
    dailyApplicationLimit: z.number().int().min(1).max(100),
    excludedCompanies: z.array(z.string()).optional(),
    minimumSalary: z.number().min(0).optional(),
    preferredLocations: z.array(z.string()).optional(),
    autoApplyEnabled: z.boolean(),
    requireApproval: z.boolean()
});

module.exports = {
    alertSchema,
    profileUpdateSchema,
    applicationStatusSchema,
    applicationNotesSchema,
    savedJobSchema,
    jobSearchAdvancedSchema,
    educationSchema,
    experienceSchema,
    skillsSchema,
    companyReviewSchema,
    insiderConnectionSchema,
    agentPreferencesSchema
};
