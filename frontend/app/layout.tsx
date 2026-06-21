import "./globals.css";

export const metadata = {
  title: "AI HR Platform",
  description: "Simple AI-powered hiring workflow"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
