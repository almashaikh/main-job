# SkillSphere - AI-Powered Career Development Platform

A modern Next.js frontend application for career development with AI-powered features including resume building, learning roadmaps, skill gap analysis, and more.

## 🚀 Features

- **Landing Page**: Beautiful, responsive landing page with features showcase
- **Authentication**: Modern login page with social authentication options
- **Dashboard Layout**: Professional sidebar navigation with mobile responsiveness
- **Dashboard Pages**:
  - **Home**: Overview with stats, recommendations, and quick actions
  - **Learning Roadmap**: Personalized learning paths with progress tracking
  - **Gap Analyzer**: Skill comparison and personalized recommendations
  - AI Resume Builder (coming soon)
  - Career Recommender (coming soon)
  - Job Opportunities (coming soon)
  - And more...

## 🛠️ Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Deployment**: Vercel (recommended)

## 📦 Installation

1. **Install dependencies**:
```bash
npm install
```

2. **Run the development server**:
```bash
npm run dev
```

3. **Open your browser**:
Navigate to [http://localhost:3000](http://localhost:3000)

## 📁 Project Structure

```
frontend/
├── app/
│   ├── dashboard/
│   │   ├── home/
│   │   │   └── page.tsx          # Dashboard home page
│   │   ├── roadmap/
│   │   │   └── page.tsx          # Learning roadmap
│   │   ├── gap-analyzer/
│   │   │   └── page.tsx          # Skill gap analyzer
│   │   ├── layout.tsx            # Dashboard layout with sidebar
│   │   └── page.tsx              # Dashboard redirect
│   ├── login/
│   │   └── page.tsx              # Login page
│   ├── globals.css               # Global styles
│   ├── layout.tsx                # Root layout
│   └── page.tsx                  # Landing page
├── public/                        # Static assets
├── package.json
├── tsconfig.json
├── tailwind.config.ts
└── next.config.js
```

## 🎨 Design Features

- **Dark Theme**: Modern dark UI with gradient accents
- **Responsive**: Fully responsive design for all screen sizes
- **Mobile-First**: Collapsible sidebar for mobile devices
- **Smooth Transitions**: Professional animations and hover effects
- **Accessible**: Semantic HTML and keyboard navigation support

## 🚦 Available Routes

- `/` - Landing page (Public)
- `/login` - Login page (Public)
- `/dashboard` - Redirects to `/dashboard/home`
- `/dashboard/home` - Dashboard overview (Protected)
- `/dashboard/roadmap` - Learning roadmap (Protected)
- `/dashboard/gap-analyzer` - Skill gap analysis (Protected)

## 🔧 Customization

### Colors
Edit `tailwind.config.ts` to customize the color scheme.

### Navigation
Update the navigation items in `app/dashboard/layout.tsx`.

### Content
Modify the page content in respective `page.tsx` files.

## 📝 Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## 🌐 Deployment

### Deploy to Vercel (Recommended)

1. Push your code to GitHub
2. Import your repository in Vercel
3. Deploy with one click

### Deploy to Other Platforms

Build the application:
```bash
npm run build
```

The output will be in the `.next` folder.

## 🎯 Next Steps

1. **Add Authentication**: Integrate with your backend API or auth service
2. **Connect Backend**: Add API calls to your backend services
3. **Add More Pages**: Implement remaining dashboard pages
4. **Add State Management**: Consider Redux, Zustand, or Context API
5. **Add Forms**: Implement resume builder and other interactive features
6. **Add Testing**: Set up Jest and React Testing Library

## 📄 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

Built with ❤️ using Next.js and Tailwind CSS
