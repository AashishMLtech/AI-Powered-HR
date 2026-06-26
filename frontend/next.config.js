/** @type {import('next').NextConfig} */
const backendUrl = process.env.BACKEND_URL || "https://ai-powered-hr.onrender.com";

const nextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/v1/:path*",
        destination: `${backendUrl}/api/v1/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
