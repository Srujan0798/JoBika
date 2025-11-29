/**
 * Indian Market Formatters & Utilities
 * Handles currency, salary, experience, and other India-specific formatting
 */

// Currency Formatting
export function formatSalary(min, max, period = 'yearly') {
    if (!min && !max) return 'Not disclosed';

    if (period === 'yearly') {
        // Convert to LPA (Lakhs Per Annum)
        const minLPA = min ? (min / 100000).toFixed(1) : null;
        const maxLPA = max ? (max / 100000).toFixed(1) : null;

        if (minLPA && maxLPA) {
            return `₹${minLPA}-${maxLPA} LPA`;
        } else if (maxLPA) {
            return `Up to ₹${maxLPA} LPA`;
        } else if (minLPA) {
            return `₹${minLPA}+ LPA`;
        }
    } else if (period === 'monthly') {
        const minK = min ? (min / 1000).toFixed(0) : null;
        const maxK = max ? (max / 1000).toFixed(0) : null;

        if (minK && maxK) {
            return `₹${minK}-${maxK}K/month`;
        }
        return `₹${minK || maxK}K/month`;
    }

    return 'Not disclosed';
}

// CTC Breakdown
export function formatCTCBreakdown(ctc) {
    const annual = ctc;
    const monthly = ctc / 12;
    const inHand = monthly * 0.7; // Approximate take-home (70% of gross)

    return {
        annual: `₹${(annual / 100000).toFixed(2)} LPA`,
        monthly: `₹${(monthly / 1000).toFixed(1)}K/month`,
        inHand: `₹${(inHand / 1000).toFixed(1)}K/month (approx. in-hand)`
    };
}

// Experience Formatting
export function formatExperience(months) {
    if (!months || months === 0) return 'Fresher';

    const years = Math.floor(months / 12);
    const remainingMonths = months % 12;

    if (years === 0) {
        return `${remainingMonths} ${remainingMonths === 1 ? 'month' : 'months'}`;
    }

    if (remainingMonths === 0) {
        return `${years} ${years === 1 ? 'year' : 'years'}`;
    }

    return `${years}.${remainingMonths} years`;
}

// Notice Period Formatting
export function formatNoticePeriod(days) {
    if (!days || days === 0) return 'Immediate joiner';
    if (days === 15) return '15 days';
    if (days === 30) return '1 month';
    if (days === 60) return '2 months';
    if (days === 90) return '3 months';
    return `${days} days`;
}

// Company Type
export function formatCompanyType(type) {
    const types = {
        'mnc': 'MNC',
        'indian_it_services': 'Indian IT Services',
        'product': 'Product Company',
        'startup': 'Startup',
        'psu': 'PSU',
        'government': 'Government',
        'mid_size': 'Mid-size Company'
    };
    return types[type] || type;
}

// Education Grading
export function formatGrade(value, type) {
    if (type === 'percentage') return `${value}%`;
    if (type === 'cgpa_10') return `${value}/10 CGPA`;
    if (type === 'cgpa_4') return `${value}/4.0 GPA`;
    return value;
}

// Location Tier
export function getLocationTier(city) {
    const tier1 = ['Mumbai', 'Delhi', 'NCR', 'Bangalore', 'Bengaluru', 'Hyderabad', 'Chennai', 'Pune', 'Kolkata'];
    const tier2 = ['Ahmedabad', 'Jaipur', 'Lucknow', 'Chandigarh', 'Indore', 'Nagpur', 'Coimbatore', 'Kochi'];

    const normalized = city.toLowerCase();

    if (tier1.some(c => normalized.includes(c.toLowerCase()))) return 'Tier 1';
    if (tier2.some(c => normalized.includes(c.toLowerCase()))) return 'Tier 2';
    return 'Tier 3';
}

// Job Type Translation
export function translateJobType(type) {
    const translations = {
        'full_time': 'Full-time',
        'part_time': 'Part-time',
        'contract': 'Contract',
        'internship': 'Internship',
        'freelance': 'Freelance',
        'walkin': 'Walk-in Interview'
    };
    return translations[type] || type;
}

// Work Mode
export function formatWorkMode(mode) {
    const modes = {
        'remote': '🏠 Remote',
        'hybrid': '🔄 Hybrid',
        'onsite': '🏢 On-site',
        'wfh': '🏠 Work From Home'
    };
    return modes[mode] || mode;
}

// Date Formatting (India-specific)
export function formatDate(date) {
    const d = new Date(date);
    const options = { day: 'numeric', month: 'short', year: 'numeric' };
    return d.toLocaleDateString('en-IN', options);
}

// Phone Number Formatting
export function formatPhone(phone) {
    // Indian mobile: +91 XXXXX XXXXX
    if (phone.startsWith('+91')) {
        const num = phone.substring(3);
        return `+91 ${num.substring(0, 5)} ${num.substring(5)}`;
    }
    if (phone.length === 10) {
        return `+91 ${phone.substring(0, 5)} ${phone.substring(5)}`;
    }
    return phone;
}

// Relative Time (India timezone)
export function formatRelativeTime(date) {
    const now = new Date();
    const then = new Date(date);
    const diffMs = now - then;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
    if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} week${Math.floor(diffDays / 7) > 1 ? 's' : ''} ago`;
    return formatDate(date);
}

// Salary Negotiation Helper
export function getSalaryNegotiationTips(currentCTC, expectedCTC) {
    const increase = ((expectedCTC - currentCTC) / currentCTC) * 100;

    if (increase < 10) {
        return {
            feasibility: 'Low',
            tip: 'Less than 10% hike is below market standards. Aim for 15-20% minimum.'
        };
    } else if (increase < 20) {
        return {
            feasibility: 'Moderate',
            tip: '10-20% is standard for job changes in India. Should be achievable.'
        };
    } else if (increase < 40) {
        return {
            feasibility: 'Good',
            tip: '20-40% is a healthy jump. Be prepared to justify with skills and value.'
        };
    } else if (increase < 60) {
        return {
            feasibility: 'Ambitious',
            tip: '40-60% requires strong justification. Only if switching to higher-paying company/role.'
        };
    } else {
        return {
            feasibility: 'Very Ambitious',
            tip: '60%+ is rare. Usually only possible when switching from service to product companies or getting promoted.'
        };
    }
}

// Company Insights
export const indianCompanyInsights = {
    'TCS': { type: 'Indian IT Services', avgCTC: '3.5-7 LPA', bond: '2 years', noticePeriod: '90 days' },
    'Infosys': { type: 'Indian IT Services', avgCTC: '4-8 LPA', bond: '2 years', noticePeriod: '90 days' },
    'Wipro': { type: 'Indian IT Services', avgCTC: '3.5-7 LPA', bond: 'Varies', noticePeriod: '60-90 days' },
    'HCL': { type: 'Indian IT Services', avgCTC: '3-6 LPA', bond: 'Varies', noticePeriod: '60 days' },
    'Tech Mahindra': { type: 'Indian IT Services', avgCTC: '3.5-6.5 LPA', bond: 'Varies', noticePeriod: '60 days' },
    'Cognizant': { type: 'MNC IT Services', avgCTC: '4-7 LPA', bond: 'No', noticePeriod: '90 days' },
    'Google': { type: 'MNC Product', avgCTC: '20-45 LPA', bond: 'No', noticePeriod: '60 days' },
    'Microsoft': { type: 'MNC Product', avgCTC: '18-40 LPA', bond: 'No', noticePeriod: '60 days' },
    'Amazon': { type: 'MNC Product', avgCTC: '15-35 LPA', bond: 'No', noticePeriod: '60 days' },
    'Flipkart': { type: 'Indian Product', avgCTC: '12-30 LPA', bond: 'No', noticePeriod: '60 days' },
    'Swiggy': { type: 'Indian Product', avgCTC: '10-28 LPA', bond: 'No', noticePeriod: '30-60 days' },
    'Zomato': { type: 'Indian Product', avgCTC: '10-25 LPA', bond: 'No', noticePeriod: '30-60 days' }
};

// Export all functions
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        formatSalary,
        formatCTCBreakdown,
        formatExperience,
        formatNoticePeriod,
        formatCompanyType,
        formatGrade,
        getLocationTier,
        translateJobType,
        formatWorkMode,
        formatDate,
        formatPhone,
        formatRelativeTime,
        getSalaryNegotiationTips,
        indianCompanyInsights
    };
}
