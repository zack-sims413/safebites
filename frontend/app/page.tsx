'use client'

import { useState } from 'react'
import SearchForm from '../components/SearchForm'
import ResultCard from '../components/ResultCard'
import { SearchResult } from '../lib/types'

export default function HomePage() {
  const [results, setResults] = useState<SearchResult[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [searchPerformed, setSearchPerformed] = useState(false)

  const handleSearch = async (searchData: {
    query: string
    radiusMiles: number
    cuisine?: string
  }) => {
    setLoading(true)
    setError(null)
    setSearchPerformed(true)

    try {
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(searchData),
      })

      if (!response.ok) {
        throw new Error(`Search failed: ${response.statusText}`)
      }

      const data = await response.json()
      setResults(data.results || [])
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
      setResults([])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Find Gluten-Friendly Restaurants
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Discover restaurants that can safely accommodate gluten allergies, celiac disease, 
          and gluten intolerances. Our AI analyzes reviews to identify safe dining options.
        </p>
      </div>

      {/* Search Form */}
      <div className="max-w-2xl mx-auto">
        <SearchForm onSearch={handleSearch} loading={loading} />
      </div>

      {/* Results Section */}
      {searchPerformed && (
        <div className="space-y-6">
          {loading && (
            <div className="text-center py-12">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
              <p className="mt-2 text-gray-600">Searching for restaurants...</p>
            </div>
          )}

          {error && (
            <div className="bg-danger-50 border border-danger-200 rounded-lg p-4">
              <p className="text-danger-800">{error}</p>
            </div>
          )}

          {!loading && !error && results.length === 0 && (
            <div className="text-center py-12">
              <p className="text-gray-600">No restaurants found matching your criteria.</p>
              <p className="text-sm text-gray-500 mt-2">
                Try expanding your search radius or removing cuisine filters.
              </p>
            </div>
          )}

          {!loading && !error && results.length > 0 && (
            <div>
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-semibold text-gray-900">
                  Found {results.length} Restaurant{results.length !== 1 ? 's' : ''}
                </h2>
                <p className="text-sm text-gray-500">
                  Sorted by gluten safety confidence
                </p>
              </div>
              
              <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                {results.map((result) => (
                  <ResultCard key={result.placeId} result={result} />
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* How It Works Section */}
      {!searchPerformed && (
        <div className="mt-16">
          <h2 className="text-2xl font-semibold text-gray-900 text-center mb-8">
            How SafeBites Works
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-primary-600">1</span>
              </div>
              <h3 className="text-lg font-semibold mb-2">Search Your Area</h3>
              <p className="text-gray-600">
                Enter your location and search radius to find nearby restaurants.
              </p>
            </div>
            <div className="text-center">
              <div className="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-primary-600">2</span>
              </div>
              <h3 className="text-lg font-semibold mb-2">AI Analysis</h3>
              <p className="text-gray-600">
                Our AI analyzes restaurant reviews for gluten safety indicators.
              </p>
            </div>
            <div className="text-center">
              <div className="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-primary-600">3</span>
              </div>
              <h3 className="text-lg font-semibold mb-2">Confidence Scoring</h3>
              <p className="text-gray-600">
                Get confidence scores based on review sentiment and volume.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
} 