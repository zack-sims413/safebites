'use client'

import { useState } from 'react'
import { Search, MapPin, Utensils } from 'lucide-react'

interface SearchFormProps {
  onSearch: (data: { query: string; radiusMiles: number; cuisine?: string }) => void
  loading: boolean
}

const CUISINE_OPTIONS = [
  { value: '', label: 'Any Cuisine' },
  { value: 'pizza', label: 'Pizza' },
  { value: 'italian', label: 'Italian' },
  { value: 'chinese', label: 'Chinese' },
  { value: 'japanese', label: 'Japanese' },
  { value: 'sushi', label: 'Sushi' },
  { value: 'thai', label: 'Thai' },
  { value: 'indian', label: 'Indian' },
  { value: 'mexican', label: 'Mexican' },
  { value: 'american', label: 'American' },
  { value: 'burgers', label: 'Burgers' },
  { value: 'bbq', label: 'BBQ' },
  { value: 'mediterranean', label: 'Mediterranean' },
  { value: 'greek', label: 'Greek' },
  { value: 'seafood', label: 'Seafood' },
  { value: 'steakhouse', label: 'Steakhouse' },
  { value: 'vegetarian', label: 'Vegetarian' },
  { value: 'vegan', label: 'Vegan' },
]

const RADIUS_OPTIONS = [
  { value: 5, label: '5 miles' },
  { value: 10, label: '10 miles' },
  { value: 15, label: '15 miles' },
  { value: 25, label: '25 miles' },
  { value: 50, label: '50 miles' },
]

export default function SearchForm({ onSearch, loading }: SearchFormProps) {
  const [query, setQuery] = useState('')
  const [radiusMiles, setRadiusMiles] = useState(10)
  const [cuisine, setCuisine] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!query.trim()) {
      return
    }

    onSearch({
      query: query.trim(),
      radiusMiles,
      cuisine: cuisine || undefined,
    })
  }

  return (
    <form onSubmit={handleSubmit} className="card space-y-6">
      <div>
        <label htmlFor="location" className="block text-sm font-medium text-gray-700 mb-2">
          <MapPin className="inline w-4 h-4 mr-1" />
          Location
        </label>
        <input
          type="text"
          id="location"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter city, address, or zip code"
          className="input-field"
          required
          disabled={loading}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label htmlFor="radius" className="block text-sm font-medium text-gray-700 mb-2">
            Search Radius
          </label>
          <select
            id="radius"
            value={radiusMiles}
            onChange={(e) => setRadiusMiles(Number(e.target.value))}
            className="input-field"
            disabled={loading}
          >
            {RADIUS_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="cuisine" className="block text-sm font-medium text-gray-700 mb-2">
            <Utensils className="inline w-4 h-4 mr-1" />
            Cuisine Type (Optional)
          </label>
          <select
            id="cuisine"
            value={cuisine}
            onChange={(e) => setCuisine(e.target.value)}
            className="input-field"
            disabled={loading}
          >
            {CUISINE_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      <button
        type="submit"
        disabled={loading || !query.trim()}
        className="btn-primary w-full flex items-center justify-center"
      >
        {loading ? (
          <>
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
            Searching...
          </>
        ) : (
          <>
            <Search className="w-4 h-4 mr-2" />
            Find Restaurants
          </>
        )}
      </button>

      <div className="text-xs text-gray-500 text-center">
        <p>
          <strong>Example locations:</strong> "Atlanta, GA", "123 Main St, New York", "90210"
        </p>
      </div>
    </form>
  )
} 