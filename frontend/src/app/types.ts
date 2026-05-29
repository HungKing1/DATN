export type LawStatus = 'draft' | 'active' | 'archived';

/** Chat query mode: 'quick' → standard RAG, 'agent' → Multi-Agent LangGraph */
export type QueryMode = 'quick' | 'agent';


export interface LegalTopic {
  id: string;
  name: string;
  description: string;
}

export interface Law {
  id: string;
  lawName: string;
  lawNumber: string;
  effectiveDate: string;
  topics: string[]; // LegalTopic IDs
  status: LawStatus;
  uploadedAt: string;
}

export interface Clause {
  id: string;
  lawId: string;
  chapter: string;
  section: string;
  articleNo: string;
  clauseNo: string;
  text: string;
}

export interface Citation {
  id: string;
  clauseId: string;
  lawName: string;
  articleInfo: string; // e.g. "Article 3, Clause 1"
  text: string;
  similarityScore?: number;
}

export interface Message {
  id: string;
  role: 'user' | 'ai';
  content: string;
  citations?: Citation[];
  confidence?: number;
  suggestedQuestions?: string[];
  timestamp: string;
  isStreaming?: boolean;
}

export interface Flashcard {
  id: string;
  front: string;
  back: string;
  clauseId: string;
  topicId: string;
}

export interface QuizQuestion {
  id: string;
  question: string;
  options: string[];
  correctIndex: number;
  explanation: string;
  clauseId: string;
}

export interface UserProgress {
  userId: string;
  documentsLearned: number;
  flashcardsCompleted: number;
  studyTimeMinutes: number;
  quizzesCompleted: number;
  weeklyActivity: { day: string; minutes: number }[];
  topicsExplored: number;
}

export interface Notebook {
  id: string;
  title: string;
  emoji: string;
  createdAt: string;
  messageCount: number;
  color: string;
}

export interface Note {
  id: string;
  content: string;
  clauseId?: string;
  citationId?: string;
  createdAt: string;
  color: 'yellow' | 'blue' | 'green' | 'pink';
}

export interface AppSettings {
  aiModel: 'gpt-4o' | 'gpt-4-turbo' | 'claude-3-5-sonnet' | 'gemini-pro';
  responseStyle: 'concise' | 'detailed' | 'academic';
  autoFlashcards: boolean;
  citationsEnabled: boolean;
  studyReminders: boolean;
  soundEffects: boolean;
  compactMode: boolean;
}

export interface LegalDocumentSummary {
  id: string;
  soKyHieu: string;
  tenDayDu: string;
  loaiVanBan: string;
  coQuanBanHanh: string | null;
  ngayThongQua: string | null;
  ngayHieuLuc: string | null;
  trangThai: string;
  tongSoDieu: number;
}

export interface TocEntry {
  id: string;
  dieu: number;
  tenDieu: string;
  anchor: string;
}

export interface TocGroup {
  phan: string | null;
  chuong: string | null;
  muc: string | null;
  items: TocEntry[];
}

export interface ArticleItem {
  id: string;
  dieu: number;
  tenDieu: string;
  titleGoc: string;
  phan: string | null;
  chuong: string | null;
  muc: string | null;
  tieuMuc: string | null;
  content: string;
}

export interface LegalDocumentDetail {
  id: string;
  soKyHieu: string;
  tenDayDu: string;
  loaiVanBan: string;
  coQuanBanHanh: string | null;
  khoaQuocHoi: string | null;
  kyHop: string | null;
  ngayThongQua: string | null;
  chucDanhNguoiKy: string | null;
  tenNguoiKy: string | null;
  quocHieu: string | null;
  tieuNgu: string | null;
  canCuBanHanh: string[];
  toc: TocGroup[];
  articles: ArticleItem[];
}