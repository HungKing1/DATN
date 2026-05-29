import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router';
import { ArrowLeft, ChevronDown, ChevronRight } from 'lucide-react';
import { legalService } from '../api/legalService';
import { LegalDocumentDetail } from '../types';
import { MarkdownRenderer } from './MarkdownRenderer';
import { Button } from './ui/button';

export const LegalDocumentViewer: React.FC = () => {
  const { soKyHieu } = useParams<{ soKyHieu: string }>();
  const [doc, setDoc] = useState<LegalDocumentDetail | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();
  const [expandedGroups, setExpandedGroups] = useState<Record<number, boolean>>({});

  useEffect(() => {
    if (!soKyHieu) return;
    setIsLoading(true);
    legalService.getDocumentDetail(decodeURIComponent(soKyHieu))
      .then(res => {
        setDoc(res);
        if (res.toc && res.toc.length > 0) {
          setExpandedGroups({ 0: true });
        }
      })
      .catch(err => console.error("Error loading document detail", err))
      .finally(() => setIsLoading(false));
  }, [soKyHieu]);

  const toggleGroup = (index: number) => {
    setExpandedGroups(prev => ({ ...prev, [index]: !prev[index] }));
  };

  const scrollToAnchor = (anchor: string) => {
    const el = document.getElementById(anchor);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  if (isLoading) {
    return (
      <div className="flex h-full items-center justify-center bg-background">
        <div className="text-muted-foreground animate-pulse">Đang tải nội dung văn bản...</div>
      </div>
    );
  }

  if (!doc) {
    return (
      <div className="flex h-full items-center justify-center bg-background">
        <div className="text-muted-foreground">Không tìm thấy tài liệu.</div>
      </div>
    );
  }

  return (
    <div className="flex h-[calc(100vh-4rem)] overflow-hidden bg-background">
      {/* Sidebar TOC */}
      <div className="w-80 border-r border-border flex flex-col bg-muted/30">
        <div className="p-4 border-b border-border flex items-center gap-2">
          <Button variant="ghost" size="icon" onClick={() => navigate('/legal')} className="h-8 w-8">
            <ArrowLeft className="w-4 h-4" />
          </Button>
          <span className="font-semibold text-sm truncate">Mục lục văn bản</span>
        </div>
        
        <div className="flex-1 overflow-y-auto p-4 space-y-1">
          {doc.toc.map((group, index) => {
            const isExpanded = !!expandedGroups[index];
            const groupTitle = [group.phan, group.chuong, group.muc].filter(Boolean).join(" - ") || "Nội dung chung";
            return (
              <div key={index} className="space-y-1">
                <div 
                  className="flex items-center gap-1 cursor-pointer hover:bg-muted p-1.5 rounded-md transition-colors"
                  onClick={() => toggleGroup(index)}
                >
                  {isExpanded ? <ChevronDown className="w-4 h-4 text-muted-foreground flex-shrink-0" /> : <ChevronRight className="w-4 h-4 text-muted-foreground flex-shrink-0" />}
                  <span className="text-xs font-semibold uppercase text-foreground truncate" title={groupTitle}>{groupTitle}</span>
                </div>
                {isExpanded && (
                  <div className="pl-6 space-y-0.5 border-l border-border ml-2 mb-2">
                    {group.items.map(item => (
                      <div 
                        key={item.id}
                        className="text-sm py-1 px-2 hover:bg-muted rounded-md cursor-pointer text-muted-foreground hover:text-foreground transition-colors truncate"
                        onClick={() => scrollToAnchor(item.anchor)}
                        title={item.tenDieu}
                      >
                        Điều {item.dieu}. {item.tenDieu}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-y-auto bg-background p-8 scroll-smooth" style={{ scrollBehavior: 'smooth' }}>
        <div className="max-w-4xl mx-auto space-y-12 pb-24">
          
          {/* Header */}
          <div className="text-center space-y-8 pb-8 border-b border-border">
            <div className="flex justify-between items-start text-sm font-semibold">
              <div className="text-center flex-1">
                <div>{doc.coQuanBanHanh || "QUỐC HỘI"}</div>
                <div className="my-1">-------</div>
                <div className="text-muted-foreground font-normal">Luật số: {doc.soKyHieu}</div>
              </div>
              <div className="text-center flex-1">
                <div>{doc.quocHieu || "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM"}</div>
                <div>{doc.tieuNgu || "Độc lập - Tự do - Hạnh phúc"}</div>
                <div className="my-1">-------</div>
                <div className="text-muted-foreground italic font-normal">Hà Nội, ngày {doc.ngayThongQua || "..."}</div>
              </div>
            </div>

            <div className="space-y-4 pt-4">
              <h1 className="text-2xl font-bold uppercase">{doc.loaiVanBan}</h1>
              <h2 className="text-4xl font-bold uppercase text-primary leading-tight">{doc.tenDayDu}</h2>
            </div>
          </div>

          {/* Căn cứ ban hành */}
          {doc.canCuBanHanh && doc.canCuBanHanh.length > 0 && (
            <div className="italic text-muted-foreground space-y-3 px-8 text-center text-sm">
              {doc.canCuBanHanh.map((cc, i) => <div key={i}>{cc}</div>)}
            </div>
          )}

          {/* Articles */}
          <div className="space-y-12">
            {doc.articles.map(article => {
              // We could conditionally render part/chapter headers here, 
              // but relying on the TOC for navigation is usually sufficient.
              return (
                <div key={article.id} id={`dieu-${article.dieu}`} className="scroll-mt-6 space-y-4">
                  <h3 className="text-lg font-bold text-foreground">
                    {article.titleGoc || `Điều ${article.dieu}. ${article.tenDieu}`}
                  </h3>
                  <div className="text-foreground text-[15px] leading-loose">
                    <MarkdownRenderer content={article.content} />
                  </div>
                </div>
              );
            })}
          </div>

          {/* Footer - Signing Info */}
          <div className="pt-16 pb-8 space-y-8 text-sm">
            <div className="italic text-muted-foreground text-center">
              Luật này được {doc.coQuanBanHanh || "Quốc hội"} nước Cộng hòa xã hội chủ nghĩa Việt Nam {doc.khoaQuocHoi ? `${doc.khoaQuocHoi}, ` : ""}{doc.kyHop || ""} thông qua ngày {doc.ngayThongQua ? doc.ngayThongQua : "..."}.
            </div>
            
            <div className="flex justify-end pr-12 pt-8">
              <div className="text-center space-y-24">
                <div className="font-bold text-base">{doc.chucDanhNguoiKy || "CHỦ TỊCH QUỐC HỘI"}</div>
                <div className="font-bold text-base">{doc.tenNguoiKy || ""}</div>
              </div>
            </div>
          </div>
          
        </div>
      </div>
    </div>
  );
};
