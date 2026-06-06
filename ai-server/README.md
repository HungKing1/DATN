# AI Server (RAG & Multi-Agent Backend)

## 1. Giới thiệu
AI Server là thành phần cốt lõi xử lý các tác vụ trí tuệ nhân tạo của hệ thống, cung cấp khả năng tìm kiếm và trả lời câu hỏi pháp luật (Legal QA) dựa trên kiến trúc RAG (Retrieval-Augmented Generation) và hệ thống tác tử đa nhiệm (Multi-Agent). Backend được xây dựng bằng **FastAPI**, kết hợp với **LangChain** và **LangGraph**, đảm bảo hiệu suất cao, khả năng mở rộng tốt và thiết kế theo chuẩn **Clean Architecture**.

## 2. Chức năng AI
- **RAG Pipeline (Retrieval-Augmented Generation)**: Tìm kiếm và trích xuất thông tin từ văn bản pháp luật với độ chính xác cao.
- **Hybrid Search**: Kết hợp tìm kiếm theo từ khóa (BM25) và tìm kiếm ngữ nghĩa (Semantic Search) trên **Weaviate Vector Database**.
- **Reranking**: Xếp hạng lại kết quả truy xuất bằng mô hình Cross-Encoder để ưu tiên các đoạn văn bản có mức độ liên quan cao nhất.
- **Multi-Agent System**: Vận hành các tác tử (Agent) thông minh thông qua **LangGraph**, giúp phân tích đa chiều các câu hỏi phức tạp, tự động điều hướng tra cứu và tổng hợp câu trả lời dựa trên ngữ cảnh pháp lý.
- **Document Ingestion**: Tiền xử lý, chia nhỏ văn bản pháp luật (Chunking), nhúng (Embedding) và tự động đồng bộ tài liệu từ **MongoDB** sang kho lưu trữ **Weaviate**.

## 3. Kiến trúc hệ thống
Hệ thống tuân thủ nghiêm ngặt **Clean Architecture**, phân tách rõ ràng các thành phần để tối ưu khả năng bảo trì:
- **Presentation Layer**: Chứa API Routes, Middleware, và Exception Handlers (FastAPI).
- **Application Layer**: Chứa Controllers và Use Cases để điều phối luồng xử lý (Business Logic).
- **Domain Layer**: Định nghĩa Schemas, Entities cốt lõi, Models, và Exceptions.
- **Infrastructure Layer**: Triển khai kết nối đến Database (MongoDB, Weaviate), External APIs, và các LLM Providers (OpenAI, Gemini, Groq).
- **Dependency Injection (DI)**: Sử dụng IoC container (trong thư mục `di`) để quản lý và khởi tạo các dependencies.

**Luồng xử lý truy vấn (Query Pipeline)**:
`Request -> FastAPI Route -> AgentController -> MultiAgentService (LangGraph) -> Weaviate (Retrieval) -> Reranker -> LLM -> Response`

## 4. Mô hình sử dụng
AI Server linh hoạt hỗ trợ nhiều nhà cung cấp LLM và cấu hình mô hình (Model) khác nhau, được thiết lập thông qua `.env`:
- **LLM Providers (Tùy chọn)**: 
  - **Google Gemini** (Mặc định): `gemini-3.1-flash-lite-preview`
  - **OpenAI**: `gpt-4o`
  - **Groq**: `openai/gpt-oss-120b`
- **Embedding Model**: `all-MiniLM-L6-v2` (Sentence Transformers).
- **Reranking Model**: `cross-encoder/ms-marco-MiniLM-L-6-v2`.
- **Vector Database**: **Weaviate** (Lưu trữ Vector Embedding và thực thi Hybrid Search).
- **Primary Database**: **MongoDB** (Lưu trữ metadata và raw document gốc).

## 8. API Endpoints
Base URL mặc định: `http://localhost:8000`

### Agent Query API
- `POST /api/v1/query/agent/`: Gửi truy vấn cho hệ thống Multi-Agent và RAG. Trả lời câu hỏi kèm theo thông tin trích dẫn pháp lý.

### Ingestion API (Đồng bộ dữ liệu)
- `GET /api/v1/ingestion/laws`: Liệt kê danh sách các văn bản luật hiện đã được đánh chỉ mục trong Weaviate.
- `POST /api/v1/ingestion/laws`: Ingest (đồng bộ) một văn bản pháp luật mới từ MongoDB vào Weaviate.
- `POST /api/v1/ingestion/laws/{so_ky_hieu}/reload`: Cập nhật/ingest lại một văn bản luật (Xóa chunks cũ và thực hiện lại).
- `DELETE /api/v1/ingestion/laws/{so_ky_hieu}`: Xóa toàn bộ dữ liệu của một văn bản luật khỏi Vector DB.

### Health Check
- `GET /health`: Kiểm tra trạng thái hoạt động cơ bản của FastAPI server.
- `GET /health/ready`: Kiểm tra trạng thái kết nối tới các dịch vụ ngoại vi (Weaviate, v.v.).

## 9. Cấu trúc thư mục
```text
ai-server/
├── .env.example            # Mẫu cấu hình các biến môi trường
├── pyproject.toml          # Tệp cấu hình project và quản lý dependencies của uv
├── uv.lock                 # Lock file đảm bảo version của dependencies
└── src/
    └── rag_backend/        # Thư mục mã nguồn chính (Root module)
        ├── application/    # Controllers và Use Cases
        ├── config/         # Quản lý cấu hình, Settings
        ├── data/           # Triển khai Repositories
        ├── di/             # Dependency Injection Container
        ├── domain/         # Schemas, Pydantic Models, Exceptions
        ├── infrastructure/ # LLM clients, Database clients, Embeddings
        ├── presentation/   # API Routes (FastAPI), Middlewares
        └── main.py         # Điểm khởi chạy (Entry point) của ứng dụng
```

## 10. Cài đặt môi trường
Dự án yêu cầu **Python 3.11+** và sử dụng **[uv](https://docs.astral.sh/uv/)** làm trình quản lý package và môi trường ảo (nhanh và ổn định hơn pip/poetry).

**Bước 1: Cài đặt `uv`**
- Windows (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- macOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`

**Bước 2: Cài đặt dependencies**
Tại thư mục `ai-server`, chạy lệnh sau để `uv` tự động tạo `.venv` và đồng bộ các gói thư viện:
```bash
uv sync
```

**Bước 3: Cấu hình biến môi trường**
Sao chép file `.env.example` thành `.env`:
```bash
cp .env.example .env
```
Mở `.env` và thiết lập các thông số chính:
- Chọn `LLM_PROVIDER` (ví dụ: `google`, `openai`).
- Điền API Keys: `GOOGLE_API_KEY` hoặc `OPENAI_API_KEY`.
- Các kết nối Database: `WEAVIATE_URL` (thường là http://localhost:9090) và `MONGODB_URL`.


## 11. Cách chạy server

**Chạy môi trường Phát triển (Development Mode):**
Môi trường dev tự động hot-reload khi có thay đổi code.
```bash
uv run uvicorn rag_backend.main:app --reload --host 0.0.0.0 --port 8000
```
Sau khi server chạy, truy cập Swagger UI API Docs tại: [http://localhost:8000/docs](http://localhost:8000/docs)

## 12. Logging & Monitoring
- **Application Logging**: AI Server sử dụng thư viện `structlog` để định dạng và ghi log cấu trúc rõ ràng. Có thể tùy chỉnh độ chi tiết của log qua biến môi trường `LOG_LEVEL` (`INFO`, `DEBUG`, `ERROR`).
- **API Request Monitoring**: Sử dụng Custom Middleware (`LoggingMiddleware`) để log mọi thông tin request/response (phương thức HTTP, đường dẫn, thời gian phản hồi, trạng thái).
- **LLM & Agent Tracing (LangSmith)**:
  - Dự án được tích hợp sẵn cấu hình **LangSmith** giúp debug luồng thực thi phức tạp của LangGraph/LangChain và theo dõi chi phí sử dụng API.
  - Để kích hoạt, cấu hình trong `.env`:
    ```env
    LANGCHAIN_TRACING_V2=true
    LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
    LANGCHAIN_API_KEY="<your-langsmith-api-key>"
    LANGCHAIN_PROJECT="<your-project-name>"
    ```
