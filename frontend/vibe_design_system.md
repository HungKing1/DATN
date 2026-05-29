# 🎨 Vibe Legal - Design System & Component Guidelines

Tài liệu này định nghĩa hệ thống thiết kế toàn diện (Design System) dành cho ứng dụng **Vibe Legal**. Hệ thống này được tối ưu hóa riêng cho **Light Mode**, sử dụng **Tailwind CSS v4** và **Framer Motion**, nhằm đảm bảo tính nhất quán, chuyên nghiệp và hiệu suất cao.

---

## 1. 🌈 Design Tokens (Hệ thống biến thiết kế)

Toàn bộ design token được quản lý qua CSS Variables và map thẳng vào Tailwind v4 (`theme.css`). **Tuyệt đối không dùng mã màu hardcode (ví dụ `#f3f4f6`) trong class.**

### 1.1. Colors (Màu sắc)
Hệ thống sử dụng thang màu HSL/OKLCH cho độ chính xác cao. Tất cả các thành phần UI **chỉ hỗ trợ Light Mode**.

| Lớp màu | Token (Tailwind class) | Vai trò & Ứng dụng |
|---------|-----------------------|-------------------|
| **Background** | `bg-background` | Nền mặc định của toàn bộ trang web (trắng tinh khiết). |
| **Foreground** | `text-foreground` | Màu chữ chính, tương phản cao trên nền `background`. |
| **Primary** | `bg-primary`, `text-primary` | Nhấn mạnh thương hiệu (Buttons, Active states). |
| **Secondary** | `bg-secondary`, `text-secondary` | Nền phụ trợ, badge, hoặc các action ít quan trọng hơn. |
| **Card / Surface**| `bg-card`, `text-card-foreground` | Nền cho Card, Modal, Dropdown, Box nội dung nổi. |
| **Muted** | `bg-muted`, `text-muted-foreground` | Nền xám nhạt cho Sidebar/Section, chữ xám phụ trợ (caption, placeholder). |
| **Border & Ring**| `border-border`, `ring-ring` | Đường viền ngăn cách (divider, card border), viền focus khi nhấn tab. |
| **Accent** | `bg-accent`, `text-accent-foreground` | Hiệu ứng khi hover vào thẻ, row, hoặc button ghost. |
| **Destructive** | `bg-destructive`, `text-destructive-foreground`| Hành động nguy hiểm (Xóa, Hủy, Báo lỗi). |
| **Sidebar** | `bg-sidebar`, `text-sidebar-foreground` | Màu nền tĩnh riêng cho vùng điều hướng trái (LeftSidebar, Admin Sidebar). |

### 1.2. Typography (Kiểu chữ)
Dự án sử dụng phông chữ **Inter** hoặc **Geist** làm mặc định (sans-serif) để mang lại cảm giác hiện đại, clean.

- **h1:** `text-2xl font-bold tracking-tight` (Tiêu đề trang)
- **h2:** `text-xl font-semibold` (Tiêu đề phân khu)
- **h3:** `text-lg font-medium` (Tiêu đề Card/Modal)
- **p (Body):** `text-sm leading-relaxed text-foreground` (Nội dung chính)
- **Caption:** `text-xs text-muted-foreground` (Chú thích, nhãn thời gian)

### 1.3. Radius, Shadows & Elevations
- **Radius:** Mặc định sử dụng góc bo tròn `rounded-lg` (`0.5rem`) cho Component chuẩn, `rounded-xl` cho Modal/Card lớn, `rounded-full` cho Badge/Avatar.
- **Shadows:** Thiết kế phẳng, nổi bọt bằng đường viền mỏng + shadow rất nhạt.
  - Base: `border border-border shadow-sm`
  - Floating (Dropdown, Modal): `border border-border shadow-lg`

---

## 2. 📐 Layout & Spacing Rules

- **Container:** Nội dung chính bọc trong `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`.
- **Gaps (Spacing):** 
  - Micro: `gap-1`, `gap-2` (Giữa Icon và Text).
  - Component: `gap-4`, `gap-6` (Khoảng cách các block trong form, card).
  - Section: `gap-8`, `gap-12` (Giữa các phần lớn của trang).
- **Z-Index System:**
  - `z-10`: Sticky headers.
  - `z-40`: Overlays, Backdrops.
  - `z-50`: Modals, Dialogs, Toasts, Command Palette.

---

## 3. 🧩 Component Specifications

### 3.1. Buttons
Cấu trúc base: `inline-flex items-center justify-center rounded-lg text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50`

- **Variants:**
  - `default`: `bg-primary text-primary-foreground hover:bg-primary/90`
  - `secondary`: `bg-secondary text-secondary-foreground hover:bg-secondary/80`
  - `outline`: `border border-input bg-background hover:bg-accent hover:text-accent-foreground`
  - `ghost`: `hover:bg-accent hover:text-accent-foreground` (Chỉ có text, không nền).
  - `premium`: `bg-gradient-to-br from-blue-500 to-violet-600 text-white shadow-sm hover:opacity-90` (Dùng cho hành động AI/Submit chính).
- **Sizes:** `sm` (h-8 px-3), `default` (h-9 px-4), `lg` (h-10 px-8), `icon` (h-9 w-9).

### 3.2. Inputs & Forms
- Base: `flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50`
- **Lỗi (Error State):** Viền đỏ `border-destructive focus-visible:ring-destructive`. Luôn đi kèm `<p className="text-xs text-destructive">` giải thích lỗi bên dưới.

### 3.3. Cards & Surfaces
- Bắt buộc phải có: `bg-card text-card-foreground border border-border shadow-sm rounded-xl`.
- Interactive Card (Clickable): Thêm `hover:border-primary/50 hover:shadow-md transition-all cursor-pointer`.

---

## 4. 🖱 Interaction States (Trạng thái tương tác)

Tất cả các thành phần tương tác phải định nghĩa rõ 4 trạng thái:
1. **Hover:** Thay đổi nền (`hover:bg-accent`), mờ nhẹ (`hover:opacity-90`), hoặc trượt viền.
2. **Focus / Focus-visible:** Bắt buộc có viền bao `focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2` để hỗ trợ điều hướng bàn phím.
3. **Active (Pressed):** Thu nhỏ nhẹ (nếu dùng framer-motion `whileTap={{ scale: 0.98 }}`) hoặc đổi màu nền đậm hơn.
4. **Disabled:** Thêm `disabled:opacity-50 disabled:cursor-not-allowed`.

---

## 5. 🎬 Motion & Animation Rules

Chỉ thêm hiệu ứng vào những nơi mang lại giá trị định hướng cho người dùng (Feedback, Loading, Transitions).

- **Framer Motion (`motion/react`)**: Dành cho Modal, Layout Shifts, Page Transitions.
  - *Fade in:* `initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}`
  - *Slide up:* `initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}`
  - *Duration:* Luôn nhanh & gãy gọn (`duration: 0.2` hoặc `0.3`, dùng spring physics cho popup).
- **Tailwind Animate (`tw-animate-css`)**: Dành cho các state đơn giản bằng class.
  - Nhịp đập: `animate-pulse` (Loading skeletons, recording mic).
  - Xoay: `animate-spin` (Loader icons).

---

## 6. 🔔 Toasts & 🖼 Icons

- **Toasts (Sonner):**
  - Mọi thông báo hành động (Thành công, Thất bại, Cảnh báo) đều đẩy qua hàm `toast` của Sonner.
  - *Success:* `toast.success('Đã lưu tài liệu')`
  - *Error:* `toast.error('Lỗi kết nối', { description: 'Vui lòng thử lại' })`
- **Icons (Lucide React):**
  - Kích thước chuẩn: `w-4 h-4` cho inline text, `w-5 h-5` cho icon button.
  - Chỉ import từ `lucide-react`. Đảm bảo truyền class `flex-shrink-0` nếu icon nằm trong flex layout (để tránh bị bóp méo khi text dài).

---

## 7. ♿ Accessibility (A11y) Guidelines

Hệ thống phải thân thiện với mọi người dùng (kể cả dùng trình đọc màn hình hay bàn phím).
- **Semantics:** Dùng đúng thẻ HTML. Button là `<button>`, Link là `<a>` hoặc `<Link>`. Không gắn `onClick` vào `<div>` nếu không có `role="button"` và `tabIndex={0}`.
- **Aria Labels:** Mọi Button chỉ chứa Icon (không có chữ) BẮT BUỘC phải có `aria-label="Tên hành động"` hoặc `title`.
- **Tương phản:** Tuân thủ tỉ lệ tương phản màu của Light Mode, chữ phụ không được làm quá nhạt (tối thiểu dùng `text-muted-foreground`).

---

## 8. 📁 Coding Rules & Best Practices

### 8.1. Cấu trúc Component
- Giới hạn **dưới 200 dòng code**. Nếu to hơn, hãy tách các phần nhỏ (vd: `Header`, `Form`, `Footer`) ra file riêng hoặc function riêng cùng file.
- Luôn viết bằng **Arrow Functions**.
- Giao tiếp dữ liệu qua Props có khai báo **Interface rõ ràng**. Tuyệt đối KHÔNG DÙNG `any`.

```tsx
interface UserCardProps {
  user: UserResponse;
  onEdit?: (id: string) => void;
  className?: string;
}

export const UserCard = ({ user, onEdit, className }: UserCardProps) => {
  return (
    <div className={cn("bg-card border border-border p-4 rounded-lg", className)}>
      <p className="text-foreground font-medium">{user.email}</p>
      {/* ... */}
    </div>
  );
};
```

### 8.2. Tiện ích `cn()` (clsx + tailwind-merge)
- Bất cứ component nào nhận `className` từ bên ngoài vào đều phải được merge thông qua hàm `cn()` để ghi đè Tailwind an toàn, tránh xung đột CSS.

### 8.3. Thứ tự import
Sắp xếp file rõ ràng để dễ đọc:
1. React / Framework hooks (`useState`, `useEffect`, `react-router`).
2. Third-party libraries (`lucide-react`, `motion`, `sonner`).
3. Global Contexts / Stores (`useApp`, `useAuth`).
4. Internal Components (`../ui/button`).
5. Types & Utils (`../types`, `cn()`).

---
*(Tài liệu này là cốt lõi để duy trì UI/UX của Vibe Legal. Bất kỳ thành viên nào tham gia dự án đều phải tuân thủ nghiêm ngặt để giữ sự đồng nhất trong kiến trúc hệ thống Light Mode.)*
