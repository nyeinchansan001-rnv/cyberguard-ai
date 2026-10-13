import "./globals.css";

export const metadata = {
  title: "CyberGuard AI",
  description: "AI-powered phishing URL analyzer",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
