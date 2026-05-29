import { fetchApi } from './apiClient';
import { Law, LegalTopic, LegalDocumentSummary, LegalDocumentDetail } from '../types';

export interface PageResponse<T> {
  content: T[];
  totalElements: number;
  totalPages: number;
  number: number;
  size: number;
}

export const getLegalDocumentList = (page = 0, size = 10) =>
  fetchApi<PageResponse<LegalDocumentSummary>>(
    `/legal/documents?page=${page}&size=${size}`
  );

export const searchLegalDocuments = (keyword: string, page = 0, size = 10) =>
  fetchApi<PageResponse<LegalDocumentSummary>>(
    `/legal/documents/search?keyword=${encodeURIComponent(keyword)}&page=${page}&size=${size}`
  );

export const getLegalDocumentDetail = (soKyHieu: string) =>
  fetchApi<LegalDocumentDetail>(
    `/legal/documents/detail?soKyHieu=${encodeURIComponent(soKyHieu)}`
  );

export const legalService = {
  getLaws: () => fetchApi<Law[]>('/laws'),
  getLegalTopics: () => fetchApi<LegalTopic[]>('/topics'),
  getLawClauses: (lawId: string) => fetchApi<any[]>(`/laws/${lawId}/clauses`),
  getDocumentList: getLegalDocumentList,
  searchDocuments: searchLegalDocuments,
  getDocumentDetail: getLegalDocumentDetail,
};
