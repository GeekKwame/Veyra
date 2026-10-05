const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8001/api/v1';

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: 'LEARNER' | 'CURATOR' | 'ADMIN';
  profile?: {
    bio: string;
    avatar_url: string;
    available_hours_per_week: number;
    learning_style: string;
    timezone: string;
    public_portfolio_enabled: boolean;
  };
  created_at: string;
}

export interface Resource {
  id: string;
  title: string;
  url: string;
  provider_name: string;
  resource_type: string;
  estimated_minutes: number;
  is_completely_free: boolean;
  verification_status: string;
}

export interface Topic {
  id: string;
  title: string;
  description: string;
  sort_order: number;
  resources: Resource[];
}

export interface Skill {
  id: string;
  slug: string;
  title: string;
  description: string;
  taxonomy: 'REMEMBER' | 'UNDERSTAND' | 'APPLY' | 'ANALYZE' | 'EVALUATE' | 'CREATE';
  estimated_hours: number;
  prerequisites: string[];
  topics: Topic[];
}

export interface CompetencyArea {
  id: string;
  title: string;
  description: string;
  sort_order: number;
  skills: Skill[];
}

export interface CareerListItem {
  id: string;
  slug: string;
  title: string;
  description: string;
  industry_category: string;
  avg_months_to_complete: number;
  badge: string;
  total_skills: number;
  total_estimated_hours: number;
}

export interface CareerDetail extends CareerListItem {
  competencies: CompetencyArea[];
  milestones: string[][];
}

export interface DiscoveryRecommendation {
  career_id: string;
  slug: string;
  title: string;
  category: string;
  badge: string;
  match_percentage: number;
  estimated_months: number;
  rationale: string;
}

export interface UserSkillProgress {
  id: string;
  skill: Skill;
  status: 'LOCKED' | 'AVAILABLE' | 'IN_PROGRESS' | 'PRACTICING' | 'ASSESSED' | 'MASTERED';
  score_percentage: number;
  mastered_at: string | null;
  updated_at: string;
}

export interface UserRoadmap {
  id: string;
  career: string;
  career_title: string;
  career_slug: string;
  committed_hours_per_week: number;
  projected_completion_date: string | null;
  readiness_score: number;
  is_active: boolean;
  started_at: string;
  progress_summary: {
    total: number;
    mastered: number;
    in_progress: number;
    available: number;
    locked: number;
    completion_pct: number;
  };
  skill_progresses: UserSkillProgress[];
}

class ApiClient {
  private getHeaders(): HeadersInit {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('veyra_token');
      if (token) {
        headers['Authorization'] = `Token ${token}`;
      }
    }
    return headers;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    const response = await fetch(url, {
      ...options,
      headers: {
        ...this.getHeaders(),
        ...options.headers,
      },
    });

    if (!response.ok) {
      let errorMessage = `API Error ${response.status}: ${response.statusText}`;
      try {
        const errorData = await response.json();
        errorMessage = errorData.error || errorData.detail || JSON.stringify(errorData);
      } catch {
        // use default error message
      }
      throw new Error(errorMessage);
    }

    return response.json();
  }

  // Authentication
  async register(data: { email: string; full_name: string; password: string }) {
    const res = await this.request<{ user: User; token: string; message: string }>('/auth/register/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
    if (typeof window !== 'undefined' && res.token) {
      localStorage.setItem('veyra_token', res.token);
    }
    return res;
  }

  async login(data: { email: string; password: string }) {
    const res = await this.request<{ user: User; token: string; message: string }>('/auth/login/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
    if (typeof window !== 'undefined' && res.token) {
      localStorage.setItem('veyra_token', res.token);
    }
    return res;
  }

  async logout() {
    try {
      await this.request('/auth/logout/', { method: 'POST' });
    } finally {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('veyra_token');
      }
    }
  }

  async getMe(): Promise<User | null> {
    if (typeof window !== 'undefined' && !localStorage.getItem('veyra_token')) {
      return null;
    }
    try {
      return await this.request<User>('/auth/me/');
    } catch {
      return null;
    }
  }

  // Careers & Discovery
  async listCareers(): Promise<CareerListItem[]> {
    return this.request<CareerListItem[]>('/careers/');
  }

  async getCareerBySlug(slug: string): Promise<CareerDetail> {
    return this.request<CareerDetail>(`/careers/${slug}/`);
  }

  async evaluateDiscovery(data: {
    interests: string[];
    available_hours_per_week: number;
    work_style: string;
    environment: string;
  }): Promise<{ recommendations: DiscoveryRecommendation[] }> {
    return this.request<{ recommendations: DiscoveryRecommendation[] }>('/careers/discovery/evaluate/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Roadmaps & Pacing
  async getActiveRoadmap(): Promise<UserRoadmap> {
    return this.request<UserRoadmap>('/roadmaps/active/');
  }

  async enroll(careerId: string, hoursPerWeek: number = 10): Promise<UserRoadmap> {
    return this.request<UserRoadmap>('/roadmaps/enroll/', {
      method: 'POST',
      body: JSON.stringify({
        career_id: careerId,
        committed_hours_per_week: hoursPerWeek,
      }),
    });
  }

  async recalibratePacing(hoursPerWeek: number): Promise<{ detail: string; committed_hours_per_week: number; projected_completion_date: string }> {
    return this.request<{ detail: string; committed_hours_per_week: number; projected_completion_date: string }>('/roadmaps/recalibrate/', {
      method: 'PATCH',
      body: JSON.stringify({ hours_per_week: hoursPerWeek }),
    });
  }
}

export const api = new ApiClient();
