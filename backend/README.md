# 🚀Backend Service

Đây là service Backend của hệ thống, đóng vai trò là core service quản lý dữ liệu, xác thực người dùng và làm cầu nối giao tiếp với hệ thống AI Server (RAG & Multi-Agent LangGraph) nhằm cung cấp trải nghiệm tìm kiếm và tra cứu văn bản pháp luật thông minh.

---

## 🛠 1. Công nghệ sử dụng

Dự án được xây dựng với các công nghệ và thư viện hiện đại để đảm bảo hiệu suất, bảo mật và khả năng mở rộng:

- **Ngôn ngữ:** Java 17
- **Framework:** Spring Boot 3.x
  - **Spring Web** (Xây dựng RESTful API)
  - **Spring Security** (Xác thực và phân quyền người dùng)
  - **Spring Data MongoDB** (Tương tác cơ sở dữ liệu)
  - **Spring WebFlux / WebClient** (Gọi API đồng bộ/bất đồng bộ sang AI Server)
- **Cơ sở dữ liệu:** MongoDB (Atlas/Local)
- **Công cụ build:** Maven
- **Tiện ích:** Lombok (Giảm thiểu boilerplate code)

---

## 📁 2. Cấu trúc thư mục

Kiến trúc ứng dụng tuân thủ mô hình **Controller - Service - Repository** truyền thống, giúp dễ dàng bảo trì và mở rộng:

```text
backend/src/main/java/com/example/backend/
├── config/       # Các lớp cấu hình (CORS, Security, Bean cấu hình ứng dụng)
├── controller/   # Lớp giao tiếp API (Xử lý các request từ Frontend)
├── dto/          # Data Transfer Objects (Request/Response payload)
├── entity/       # Các Entity (Document mapping với MongoDB)
├── exception/    # Quản lý lỗi tập trung (Global Exception Handler)
├── mapper/       # Map dữ liệu giữa Entity và DTO
├── repository/   # Lớp tương tác với cơ sở dữ liệu MongoDB
├── security/     # Cấu hình Spring Security, quản lý Session/Cookie
├── service/      # Business logic, xử lý nghiệp vụ chính
└── util/         # Các tiện ích (Utils) dùng chung
```

---

## ⚙️ 3. Yêu cầu cài đặt

Để chạy dự án, máy tính của bạn cần cài đặt sẵn:

- **Java 17** (hoặc mới hơn)
- **Maven 3.8+**
- **MongoDB** (Hoặc cấu hình chuỗi kết nối MongoDB Atlas)

---

## 🚀 4. Cách chạy dự án local

### Cài đặt dependencies và chạy qua Maven

Chạy lệnh sau tại thư mục gốc của backend (`/backend`):

```bash
# Tải dependency và chạy trực tiếp
./mvnw spring-boot:run
```

### Hoặc Build ra file .jar để chạy độc lập

```bash
# Build dự án (bỏ qua tests để build nhanh hơn nếu cần bằng -DskipTests)
./mvnw clean install

# Chạy file .jar
java -jar target/backend-0.0.1-SNAPSHOT.jar
```

Mặc định, server sẽ khởi chạy tại: `http://localhost:8080`

---

## 🔐 5. Biến môi trường (`application.properties`)

Dự án cấu hình trực tiếp qua file `src/main/resources/application.properties`. Dưới đây là các cấu hình quan trọng bạn cần lưu ý:

```properties
# ===============================
# SERVER CONFIGURATION
# ===============================
server.port=8080

# Cấu hình upload file
spring.servlet.multipart.max-file-size=50MB
spring.servlet.multipart.max-request-size=100MB

# ===============================
# MONGODB CONFIGURATION
# ===============================
# Thay URI bên dưới bằng URI MongoDB của bạn
spring.mongodb.uri=mongodb+srv://<username>:<password>@cluster0.mongodb.net/datn_db?retryWrites=true&w=majority

# ===============================
# SECURITY & AUTHENTICATION
# ===============================
auth.cookie.name=SESSION_ID
auth.cookie.max-age=604800
auth.cookie.secure=false    # Đặt thành true khi deploy production (HTTPS)
auth.cookie.http-only=true

# ===============================
# AI SERVER (RAG Backend Connection)
# ===============================
# Đường dẫn tới server FastAPI (AI Server)
ai-server.base-url=http://localhost:8000
ai-server.timeout=60000        # Timeout cho truy vấn RAG tiêu chuẩn
ai-server.agent-timeout=300000 # Timeout cho truy vấn Multi-Agent (LangGraph)
```

---

## 🌐 6. API Endpoints

Hệ thống cung cấp các nhóm API chính sau (Prefix chung: `/api/v1`):

### 🔑 Authentication (`/api/v1/auth`)
- `POST /register` : Đăng ký tài khoản người dùng.
- `POST /login` : Đăng nhập (Set HttpOnly Cookie `SESSION_ID`).
- `POST /logout` : Đăng xuất (Xoá Cookie).
- `GET /me` : Lấy thông tin user đang đăng nhập.

### 💬 Chat & AI (`/api/v1/chat` & `/api/v1/conversations`)
- `POST /chat` : Tương tác với trợ lý ảo pháp luật (Route payload qua AI Server).
- `GET /conversations` : Lấy danh sách lịch sử các phiên chat.
- `GET /conversations/{id}` : Xem chi tiết một phiên chat.

### 🏛 Legal Data (`/api/v1/legal`)
- `GET /legal/documents` : Lấy danh sách văn bản pháp luật (Có phân trang).
- `GET /legal/documents/search` : Tìm kiếm văn bản bằng từ khoá.
- `GET /legal/documents/detail` : Xem chi tiết văn bản thông qua `soKyHieu`.

### 🛡 Admin & System (`/api/v1/admin`)
- `GET /admin/laws` : Lấy danh sách các tài liệu trong Vector DB (Weaviate).
- `POST /admin/laws` : Đồng bộ (Ingest) tài liệu từ MongoDB sang Vector DB.
- `POST /admin/laws/reload` : Tải lại/Cập nhật tài liệu.
- `DELETE /admin/laws` : Xoá tài liệu khỏi Vector DB.
- `GET /admin/ai-health` : Kiểm tra trạng thái hoạt động của AI Server.

---

## 🛡 7. Authentication & Authorization

Backend sử dụng cơ chế **Cookie-based Session** với Spring Security để bảo mật.

1. Khi người dùng gọi `/api/v1/auth/login` thành công, Backend sẽ tạo một định danh và gán vào một Cookie tên là `SESSION_ID`.
2. Cookie này được cấu hình **HttpOnly**, ngăn chặn việc bị đánh cắp thông qua mã độc XSS từ Frontend.
3. Trong các request tiếp theo tới các API cần bảo vệ (như Chat, Profile, Admin), trình duyệt sẽ tự động đính kèm Cookie này để Backend xác thực.

---

## 🗄 8. Database

Hệ thống sử dụng kiến trúc **Hai Cơ Sở Dữ Liệu**:

1. **MongoDB (Primary DB - Spring Boot quản lý):**
   - Nơi lưu trữ thông tin Người dùng (`User`).
   - Lưu trữ Hội thoại và Tin nhắn chat (`Conversation`, `Message`).
   - Lưu trữ nội dung nguyên bản của các Văn bản pháp luật (`LegalDocument`).
2. **Weaviate (Vector DB - AI Server quản lý):**
   - Lưu trữ các Chunk dữ liệu của văn bản pháp luật (Dưới dạng Vector Embeddings).
   - Spring Boot sẽ không giao tiếp trực tiếp với Weaviate, mà gọi API của Admin qua AI Server để ra lệnh đồng bộ hoặc xóa dữ liệu.
