/**
 * LinkedIn Networking & Referral Helper for JoBika
 * Find connections at target companies and generate referral messages
 * Tailored for Indian professional network
 */

class NetworkingHelper {
    constructor() {
        this.linkedInEndpoint = '/api/linkedin/connections'; // Future backend integration
    }

    /**
     * Find connections at a company (mock for now)
     * In production, this would integrate with LinkedIn API
     */
    async findConnectionsAtCompany(companyName, userProfile) {
        // Mock data - In production, this would call LinkedIn API
        const mockConnections = this.generateMockConnections(companyName);

        return {
            company: companyName,
            totalConnections: mockConnections.length,
            connections: mockConnections,
            alumni: this.findAlumni(mockConnections, userProfile),
            recommendations: this.rankConnections(mockConnections, userProfile)
        };
    }

    /**
     * Generate mock connections (for demonstration)
     */
    generateMockConnections(companyName) {
        const roles = [
            'Software Engineer', 'Senior SDE', 'Engineering Manager',
            'Product Manager', 'Tech Lead', 'HR Manager',
            'Recruiter', 'Team Lead', 'Director Engineering'
        ];

        const connections = [];
        const connectionCount = Math.floor(Math.random() * 5) + 1;

        for (let i = 0; i < connectionCount; i++) {
            connections.push({
                id: `conn_${i}`,
                name: this.generateIndianName(),
                role: roles[Math.floor(Math.random() * roles.length)],
                company: companyName,
                degree: Math.random() > 0.5 ? '1st' : '2nd',
                college: this.getRandomCollege(),
                yearsAtCompany: Math.floor(Math.random() * 5) + 1,
                linkedInUrl: `https://linkedin.com/in/example${i}`,
                mutualConnections: Math.floor(Math.random() * 20),
                canMessage: Math.random() > 0.3
            });
        }

        return connections;
    }

    /**
     * Find alumni from user's college
     */
    findAlumni(connections, userProfile) {
        const userCollege = userProfile.college || '';
        if (!userCollege) return [];

        return connections.filter(conn =>
            conn.college && conn.college.toLowerCase() === userCollege.toLowerCase()
        );
    }

    /**
     * Rank connections by likelihood of referral
     */
    rankConnections(connections, userProfile) {
        return connections.map(conn => ({
            ...conn,
            referralScore: this.calculateReferralScore(conn, userProfile)
        })).sort((a, b) => b.referralScore - a.referralScore);
    }

    /**
     * Calculate referral probability score
     */
    calculateReferralScore(connection, userProfile) {
        let score = 50; // Base score

        // 1st degree connections are easier to reach
        if (connection.degree === '1st') score += 30;

        // Alumni connections are more likely to help
        if (connection.college === userProfile.college) score += 25;

        // More mutual connections = stronger relationship
        score += Math.min(connection.mutualConnections * 2, 20);

        // Can message directly = easier outreach
        if (connection.canMessage) score += 15;

        // Longer at company = better understanding of culture/hiring
        score += Math.min(connection.yearsAtCompany * 5, 15);

        return Math.min(score, 100);
    }

    /**
     * Generate personalized referral request message
     */
    generateReferralMessage(connection, job, userProfile, messageType = 'professional') {
        const templates = {
            'alumni': this.getAlumniTemplate(connection, job, userProfile),
            'professional': this.getProfessionalTemplate(connection, job, userProfile),
            'mutual': this.getMutualConnectionTemplate(connection, job, userProfile),
            'cold': this.getColdOutreachTemplate(connection, job, userProfile)
        };

        // Auto-select best template
        if (connection.college === userProfile.college) {
            return templates.alumni;
        } else if (connection.mutualConnections > 5) {
            return templates.mutual;
        } else if (connection.degree === '1st') {
            return templates.professional;
        } else {
            return templates.cold;
        }
    }

    /**
     * Alumni template (most personal)
     */
    getAlumniTemplate(connection, job, userProfile) {
        return `Hi ${connection.name},

I hope this message finds you well!

I'm ${userProfile.name || 'a fellow alumnus'}, and I also graduated from ${connection.college}. I noticed you're currently working at ${connection.company} as a ${connection.role}.

I'm currently exploring opportunities in ${job.title} roles, and I came across an opening at ${connection.company} that aligns well with my background. With ${userProfile.yearsOfExperience} years of experience in ${this.getTopSkills(userProfile)}, I believe I would be a strong fit for the team.

Given our shared background at ${connection.college}, I was wondering if you'd be open to:
1. Sharing insights about the team culture and work environment
2. Potentially referring me for the ${job.title} position, if you feel it's appropriate

I'd be happy to send over my resume and discuss my experience further. I completely understand if you're not in a position to help, but I'd really appreciate any guidance you could offer.

Looking forward to hearing from you!

Best regards,
${userProfile.name}
${userProfile.phone ? `\n${userProfile.phone}` : ''}
${userProfile.email ? `\n${userProfile.email}` : ''}`;
    }

    /**
     * Professional template (1st degree connection)
     */
    getProfessionalTemplate(connection, job, userProfile) {
        return `Hi ${connection.name},

I hope you're doing well!

I noticed you're working at ${connection.company} and wanted to reach out regarding a ${job.title} opportunity I came across.

With ${userProfile.yearsOfExperience} years of experience in ${this.getTopSkills(userProfile)}, I'm actively looking for new challenges where I can contribute meaningfully. I'm particularly interested in ${connection.company} because of its ${this.getCompanyHighlight(job)}.

I'd love to learn more about:
• The team culture and working style at ${connection.company}
• The ${job.title} role and what success looks like in this position
• Whether you'd be willing to refer me, if you think I might be a good fit

I'd be happy to share my resume and discuss how my experience aligns with the role. No pressure at all if this isn't the right time!

Thanks for considering, and looking forward to connecting!

Best regards,
${userProfile.name}`;
    }

    /**
     * Mutual connections template
     */
    getMutualConnectionTemplate(connection, job, userProfile) {
        return `Hi ${connection.name},

I hope this message finds you well!

I noticed we have ${connection.mutualConnections} mutual connections, and I wanted to reach out about a ${job.title} position at ${connection.company}.

A bit about me: I have ${userProfile.yearsOfExperience} years of experience working with ${this.getTopSkills(userProfile)}. I'm currently looking for opportunities where I can leverage my skills in ${job.title} roles.

I came across the opening at ${connection.company}, and given your experience there as a ${connection.role}, I thought you might be able to provide some valuable insights about:
• The team structure and culture
• What ${connection.company} looks for in candidates
• Whether you'd be open to referring me if you think I'd be a good fit

I'd really appreciate any guidance or advice you could share. I'm happy to send my resume over for you to review.

Thank you for your time and consideration!

Best regards,
${userProfile.name}`;
    }

    /**
     * Cold outreach template (2nd degree or no connection)
     */
    getColdOutreachTemplate(connection, job, userProfile) {
        return `Hi ${connection.name},

I hope you don't mind me reaching out!

My name is ${userProfile.name}, and I'm currently exploring ${job.title} opportunities. I came across ${connection.company} and was really impressed by ${this.getCompanyHighlight(job)}.

I have ${userProfile.yearsOfExperience} years of experience in ${this.getTopSkills(userProfile)}, and I believe my background aligns well with the ${job.title} role I saw posted.

I understand you're busy, but I was hoping to ask:
• What's it like working at ${connection.company}?
• Any advice for someone applying for the ${job.title} position?

I'd be grateful for any insights you could share. If you're open to it, I can send over my resume as well.

Thank you so much for your time!

Best regards,
${userProfile.name}
${userProfile.email || ''}`;
    }

    /**
     * Generate follow-up message (if no response after 7 days)
     */
    generateFollowUpMessage(connection, userProfile) {
        return `Hi ${connection.name},

I hope you're doing well!

I wanted to follow up on my previous message about the opportunity at ${connection.company}. I completely understand you might be busy, so no worries if you haven't had a chance to respond.

I'm still very interested in learning more about ${connection.company} and the role. If you have a few minutes in the coming days, I'd really appreciate any insights you could share.

Thanks again!

Best regards,
${userProfile.name}`;
    }

    /**
     * Generate thank you message (after referral)
     */
    generateThankYouMessage(connection, userProfile) {
        return `Hi ${connection.name},

I wanted to take a moment to sincerely thank you for taking the time to refer me for the position at ${connection.company}. I really appreciate your support!

I've submitted my application and am looking forward to the possibility of joining the team. Regardless of the outcome, I'm grateful for your help and the insights you shared.

Please let me know if there's ever anything I can do to return the favor!

Warm regards,
${userProfile.name}`;
    }

    // Helper methods
    getTopSkills(userProfile) {
        const skills = userProfile.skills || [];
        const skillsList = Array.isArray(skills) ? skills : skills.split(',').map(s => s.trim());
        return skillsList.slice(0, 3).join(', ');
    }

    getCompanyHighlight(job) {
        const highlights = {
            'startup': 'innovative products and fast-paced environment',
            'mnc': 'global impact and scale',
            'product': 'focus on building world-class products',
            'fintech': 'work on cutting-edge financial technology',
            'ecommerce': 'revolutionizing online shopping in India'
        };
        return highlights[job.companySize] || 'strong reputation and culture';
    }

    generateIndianName() {
        const firstNames = ['Rahul', 'Priya', 'Amit', 'Sneha', 'Vikram', 'Ananya', 'Rohan', 'Isha'];
        const lastNames = ['Sharma', 'Kumar', 'Patel', 'Singh', 'Reddy', 'Iyer', 'Chopra', 'Mehta'];
        return `${firstNames[Math.floor(Math.random() * firstNames.length)]} ${lastNames[Math.floor(Math.random() * lastNames.length)]}`;
    }

    getRandomCollege() {
        const colleges = [
            'IIT Delhi', 'IIT Bombay', 'IIT Bangalore', 'BITS Pilani',
            'NIT Trichy', 'IIIT Hyderabad', 'VIT Vellore', 'Delhi University'
        ];
        return colleges[Math.floor(Math.random() * colleges.length)];
    }

    /**
     * Copy message to clipboard
     */
    async copyToClipboard(message) {
        try {
            await navigator.clipboard.writeText(message);
            return true;
        } catch (error) {
            console.error('Failed to copy:', error);
            return false;
        }
    }
}

// Export for use in app
if (typeof module !== 'undefined' && module.exports) {
    module.exports = NetworkingHelper;
} else {
    window.NetworkingHelper = NetworkingHelper;
}
