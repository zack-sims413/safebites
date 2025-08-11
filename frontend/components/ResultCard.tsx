'use client'

import { useState } from 'react'
import { MapPin, Star, ExternalLink, ChevronDown, ChevronUp } from 'lucide-react'
import { SearchResult } from '../lib/types'
import ConfidenceBadge from './ConfidenceBadge'

interface ResultCardProps {
  result: SearchResult
}

export default function ResultCard({ result }: ResultCardProps) {
  const [expanded, setExpanded] = useState(false)

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 80) return 'success'
    if (confidence >= 60) return 'warning'
    return 'danger'
  }

  const confidenceColor = getConfidenceColor(result.confidence)

  return (
    <div className="card hover:shadow-md transition-shadow duration-200">
      {/* Header */}
      <div className="flex justify-between items-start mb-4">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 mb-1">
            {result.name}
          </h3>
          <div className="flex items-center text-sm text-gray-600 mb-2">
            <MapPin className="w-4 h-4 mr-1" />
            <span>{result.address}</span>
          </div>
          <div className="flex items-center gap-4 text-sm text-gray-500">
            <span>{result.distanceMiles} miles away</span>
            {result.rating && (
              <div className="flex items-center">
                <Star className="w-4 h-4 text-yellow-400 mr-1" />
                <span>{result.rating}</span>
                {result.userRatingsTotal && (
                  <span className="ml-1">({result.userRatingsTotal})</span>
                )}
              </div>
            )}
          </div>
        </div>
        <ConfidenceBadge confidence={result.confidence} />
      </div>

      {/* Summary */}
      <p className="text-sm text-gray-700 mb-4">
        {result.summary}
      </p>

      {/* Gluten Review Stats */}
      <div className="bg-gray-50 rounded-lg p-3 mb-4">
        <div className="grid grid-cols-3 gap-4 text-center text-sm">
          <div>
            <div className="font-semibold text-gray-900">{result.glutenReviewCount}</div>
            <div className="text-gray-600">Total Reviews</div>
          </div>
          <div>
            <div className="font-semibold text-success-600">{result.positiveGlutenReviews}</div>
            <div className="text-gray-600">Positive</div>
          </div>
          <div>
            <div className="font-semibold text-danger-600">{result.negativeGlutenReviews}</div>
            <div className="text-gray-600">Negative</div>
          </div>
        </div>
      </div>

      {/* Expandable Details */}
      <div className="border-t border-gray-200 pt-4">
        <button
          onClick={() => setExpanded(!expanded)}
          className="flex items-center justify-between w-full text-sm text-gray-600 hover:text-gray-900"
        >
          <span>View Details</span>
          {expanded ? (
            <ChevronUp className="w-4 h-4" />
          ) : (
            <ChevronDown className="w-4 h-4" />
          )}
        </button>

        {expanded && (
          <div className="mt-4 space-y-3 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-600">Confidence Score:</span>
              <span className="font-medium">{result.confidence}/100</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Distance:</span>
              <span className="font-medium">{result.distanceMiles} miles</span>
            </div>
            {result.rating && (
              <div className="flex justify-between">
                <span className="text-gray-600">Overall Rating:</span>
                <span className="font-medium">{result.rating}/5</span>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Action Buttons */}
      <div className="flex gap-2 mt-4 pt-4 border-t border-gray-200">
        <a
          href={result.links.provider}
          target="_blank"
          rel="noopener noreferrer"
          className="btn-secondary flex-1 flex items-center justify-center text-sm"
        >
          <ExternalLink className="w-4 h-4 mr-1" />
          View on Yelp
        </a>
        <a
          href={result.links.maps}
          target="_blank"
          rel="noopener noreferrer"
          className="btn-secondary flex-1 flex items-center justify-center text-sm"
        >
          <MapPin className="w-4 h-4 mr-1" />
          Directions
        </a>
      </div>
    </div>
  )
} 