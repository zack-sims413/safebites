interface ConfidenceBadgeProps {
  confidence: number
}

export default function ConfidenceBadge({ confidence }: ConfidenceBadgeProps) {
  const getConfidenceLevel = (score: number) => {
    if (score >= 80) return { level: 'High', color: 'success' }
    if (score >= 60) return { level: 'Medium', color: 'warning' }
    if (score >= 40) return { level: 'Low', color: 'danger' }
    return { level: 'Very Low', color: 'danger' }
  }

  const { level, color } = getConfidenceLevel(confidence)

  return (
    <div className="text-right">
      <div className={`badge badge-${color} mb-1`}>
        {confidence}/100
      </div>
      <div className="text-xs text-gray-500">
        {level} Confidence
      </div>
    </div>
  )
} 