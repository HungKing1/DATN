# Vibe Frontend - Legal & Workspace AI

## 1. Giới thiệu
Vibe Frontend là ứng dụng giao diện người dùng (Client-side) cho hệ thống tra cứu văn bản pháp luật và không gian làm việc AI. Dự án cung cấp một giao diện thân thiện, hiện đại, giúp người dùng dễ dàng tương tác với các tính năng như tìm kiếm, xem văn bản, quản lý workspace và chat với AI.

## 2. Tech Stack
- **Framework/Thư viện chính:** React 18
- **Routing:** React Router 7
- **Build Tool:** Vite 6
- **Ngôn ngữ:** TypeScript
- **Styling:** Tailwind CSS 4
- **UI Components:** Radix UI, Shadcn UI
- **Icons:** Lucide React, Material Icons (@mui/icons-material)
- **Tiện ích khác:** date-fns, react-hook-form, react-markdown, recharts, sonner (Toast notifications)

## 3. Kiến trúc dự án
Dự án được xây dựng theo kiến trúc Component-based với tư tưởng Module hóa:
- **Tách biệt logic và giao diện:** Sử dụng Hook và Context API để quản lý state và logic nghiệp vụ, giữ cho UI components được "dumb" và dễ tái sử dụng.
- **Routing phân quyền:** Hệ thống routing được phân chia rõ ràng thành các nhóm bảo vệ bằng Route Guards (Admin, Authenticated User, Guest).
- **API Services:** Giao tiếp với backend thông qua các call HTTP (Axios/Fetch), sử dụng cấu hình Proxy trong Vite (`/api` -> `http://localhost:8080`) để tránh lỗi CORS trong quá trình phát triển (Development).

## 4. Cấu trúc thư mục
```text
frontend/
├── dist/                  # Thư mục chứa code đã được build production
├── node_modules/          # Chứa các thư viện và dependencies
├── src/
│   ├── app/
│   │   ├── api/           # Chứa các service gọi API (Axios/Fetch)
│   │   ├── components/    # Chứa các component dùng chung (UI components, modals, panels)
│   │   │   └── ui/        # Chứa các base component từ Shadcn UI (button, input, dialog...)
│   │   ├── context/       # React Context (Auth, Theme, Workspace...)
│   │   ├── guards/        # Route Guards để bảo vệ các route yêu cầu quyền truy cập
│   │   ├── layouts/       # Các Layout Component (MainLayout, AuthLayout, AdminLayout)
│   │   ├── pages/         # Các trang chính của ứng dụng
│   │   │   ├── admin/     # Giao diện cho Admin (Dashboard, Ingestion)
│   │   │   ├── auth/      # Đăng nhập, đăng ký
│   │   │   ├── legal/     # Tra cứu và xem chi tiết văn bản pháp luật
│   │   │   └── workspace/ # Không gian làm việc cá nhân và chat AI
│   │   ├── routes.tsx     # Cấu hình Routing chính của ứng dụng
│   │   └── types.ts       # Định nghĩa các TypeScript interface / type chung
│   ├── styles/            # Các file CSS chung và cấu hình cho Tailwind
│   └── main.tsx           # Entry point của ứng dụng React
├── index.html             # HTML template gốc
├── package.json           # Cấu hình dependencies và scripts
├── postcss.config.mjs     # Cấu hình PostCSS
└── vite.config.ts         # Cấu hình Vite (plugins, alias path, proxy server)
```

## 5. Cài đặt

Yêu cầu môi trường:
- **Node.js**: Phiên bản 18.x trở lên
- **npm** hoặc **yarn**

Các bước cài đặt:
1. Clone dự án về máy.
2. Di chuyển vào thư mục frontend:
   ```bash
   cd frontend
   ```
3. Cài đặt các gói phụ thuộc (dependencies):
   ```bash
   npm install
   ```

## 6. Chạy development

Khởi động server phát triển nội bộ bằng Vite:
```bash
npm run dev
```
Mặc định ứng dụng sẽ chạy ở port được cấu hình bởi Vite (thường là `http://localhost:5173`).
*Lưu ý: Bạn cần chạy Backend server ở cổng 8080 để API call có thể hoạt động thành công qua cấu hình proxy.*

## 7. Build production

Để build ứng dụng thành các file tĩnh chuẩn bị cho việc deploy:
```bash
npm run build
```
Lệnh này sẽ tạo ra một thư mục `dist` chứa các file HTML, JS, CSS đã được minify và tối ưu hóa.

## 8. Routing

Cấu hình routing được định nghĩa tại `src/app/routes.tsx` gồm các nhóm chính:
- **Group 1: Auth routes** (`/auth/login`, `/auth/signup`)
  - Sử dụng `AuthLayout`.
- **Group 2: Admin routes** (`/admin`, `/admin/ingestion`)
  - Yêu cầu quyền `ROLE_ADMIN`, được bảo vệ bởi `<AdminRoute>`.
  - Sử dụng `AdminLayout`.
- **Group 3: Main App routes** (`/`, `/legal`, `/legal/:soKyHieu`)
  - Yêu cầu người dùng đã đăng nhập, được bảo vệ bởi `<ProtectedRoute>`.
  - Sử dụng `MainLayout`.

## 9. Deployment

Ứng dụng Frontend (React/Vite) sau khi build (`npm run build`) sẽ là các file tĩnh (Static files). Bạn có thể triển khai thư mục `dist` lên bất kỳ dịch vụ Web Hosting hoặc nền tảng đám mây nào như:
- **Vercel** hoặc **Netlify**: Rất phù hợp cho ứng dụng Vite/React, hỗ trợ tự động build và deploy từ Git branch.
- **Nginx/Apache**: Copy thư mục `dist` vào root directory của web server.
- **Docker**: Có thể triển khai nhanh chóng bằng việc sử dụng một Nginx container để phục vụ file tĩnh.

**Lưu ý cấu hình SPA (Single Page Application):**
Khi deploy trên các web server truyền thống (như Nginx), bạn cần cấu hình fallback URL để định tuyến lại mọi yêu cầu chưa xác định về `index.html`. Điều này giúp tránh lỗi 404 Not Found khi người dùng truy cập trực tiếp bằng đường link hoặc thực hiện reload trang.
Ví dụ đối với Nginx:
```nginx
location / {
  try_files $uri $uri/ /index.html;
}
```
