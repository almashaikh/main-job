// API configuration and helper functions
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface SkillGap {
  skill: string;
  demand_percentage: number;
  job_count: number;
  priority: string;
}

export interface GapAnalysisResponse {
  target_role: string;
  match_percentage: number;
  total_required_skills: number;
  user_skills_count: number;
  matched_skills_count: number;
  missing_skills_count: number;
  readiness_score: {
    score: number;
    level: string;
    message: string;
  };
  matched_skills_detailed: Array<{
    skill: string;
    demand_percentage: number;
    demand_level: string;
    user_level?: number;
  }>;
  skill_gaps: {
    critical: SkillGap[];
    high: SkillGap[];
    medium: SkillGap[];
    low: SkillGap[];
  };
  total_gaps_by_priority: {
    critical: number;
    high: number;
    medium: number;
    low: number;
  };
  recommendations: string[];
}

export interface UserSkill {
  name: string;
  level: number;
  category: string;
}

// API Functions
export const api = {
  // Get available target roles
  async getRoles(): Promise<string[]> {
    const response = await fetch(`${API_BASE_URL}/api/roles`);
    if (!response.ok) throw new Error('Failed to fetch roles');
    const data = await response.json();
    return data.roles;
  },

  // Analyze skill gap
  async analyzeGap(userSkills: string[], targetRole: string): Promise<GapAnalysisResponse> {
    const response = await fetch(`${API_BASE_URL}/api/gap-analysis`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_skills: userSkills,
        target_role: targetRole,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to analyze gap');
    }

    return response.json();
  },

  // Analyze with user skill levels
  async analyzeUserSkills(skills: UserSkill[], targetRole: string): Promise<GapAnalysisResponse> {
    const response = await fetch(`${API_BASE_URL}/api/user-skills-analysis`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        skills,
        target_role: targetRole,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to analyze skills');
    }

    return response.json();
  },

  // Upload resume
  async uploadResume(file: File): Promise<{ skills: string[] }> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/api/upload-resume`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to upload resume');
    }

    return response.json();
  },

  // Get market skills for a role
  async getMarketSkills(role: string): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/api/market-skills/${encodeURIComponent(role)}`);
    if (!response.ok) throw new Error('Failed to fetch market skills');
    return response.json();
  },

  // Chatbot - Send message
  async chatbotMessage(
    message: string,
    gapAnalysis: any,
    userProgress?: any,
    userName?: string,
    isRecruiter?: boolean
  ): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/api/chatbot/message`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        gap_analysis: gapAnalysis,
        user_progress: userProgress,
        user_name: userName,
        is_recruiter: isRecruiter || false,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to process chatbot message');
    }

    return response.json();
  },

  // Chatbot - Get conversation history
  async getChatbotHistory(): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/api/chatbot/history`);
    if (!response.ok) throw new Error('Failed to fetch chat history');
    return response.json();
  },

  // Chatbot - Clear history
  async clearChatbotHistory(): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/api/chatbot/clear`, {
      method: 'POST',
    });
    if (!response.ok) throw new Error('Failed to clear chat history');
    return response.json();
  },
};
