import "./globals.css";

export const metadata = {
  title: "AI HR Platform",
  description: "AI-powered hiring workflow with a polished HR dashboard"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
