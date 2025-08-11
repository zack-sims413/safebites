import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'SafeBites - Gluten-Friendly Restaurant Finder',
  description: 'Find restaurants that can safely accommodate gluten allergies, celiac disease, and gluten intolerances.',
  keywords: 'gluten-free, celiac, restaurant, allergy, safe dining',
  authors: [{ name: 'SafeBites Team' }],
  viewport: 'width=device-width, initial-scale=1',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen bg-gray-50">
          <header className="bg-white shadow-sm border-b border-gray-200">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex justify-between items-center py-4">
                <div className="flex items-center">
                  <h1 className="text-2xl font-bold text-primary-600">
                    SafeBites
                  </h1>
                  <span className="ml-2 text-sm text-gray-500">
                    Gluten-Friendly Restaurant Finder
                  </span>
                </div>
                <div className="text-sm text-gray-500">
                  <a 
                    href="/docs" 
                    className="text-primary-600 hover:text-primary-700"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    API Docs
                  </a>
                </div>
              </div>
            </div>
          </header>
          
          <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {children}
          </main>
          
          <footer className="bg-white border-t border-gray-200 mt-16">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
              <div className="text-center text-sm text-gray-500">
                <p className="mb-2">
                  <strong>Safety Disclaimer:</strong> While SafeBites analyzes reviews to identify potentially gluten-safe restaurants, 
                  we cannot guarantee 100% safety. Always contact restaurants directly to confirm their gluten-free protocols.
                </p>
                <p>
                  This tool is for informational purposes only and should not replace proper medical advice or direct communication with restaurants.
                </p>
              </div>
            </div>
          </footer>
        </div>
      </body>
    </html>
  )
} 