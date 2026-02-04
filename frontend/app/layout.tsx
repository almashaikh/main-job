import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'SkillSphere - AI-Powered Career Development',
  description: 'Build your resume, learn new skills, and advance your career with AI',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
