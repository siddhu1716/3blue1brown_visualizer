'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Textarea } from '@/components/ui/textarea'
import { Loader2, Play, Download } from 'lucide-react'

interface VisualizationResult {
  video_url: string
  refined_prompt: string
  visualization_type: string
}

export default function Home() {
  const [prompt, setPrompt] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState<VisualizationResult | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleGenerate = async () => {
    if (!prompt.trim()) return

    setIsLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      })

      if (!response.ok) {
        throw new Error('Failed to generate visualization')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setIsLoading(false)
    }
  }

  const handleDownload = () => {
    if (result?.video_url) {
      const link = document.createElement('a')
      link.href = result.video_url
      link.download = 'visualization.mp4'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Header */}
        <div className="text-center py-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Manim Visualizer
          </h1>
          <p className="text-lg text-gray-600">
            Transform natural language into beautiful mathematical animations
          </p>
        </div>

        {/* Input Section */}
        <Card>
          <CardHeader>
            <CardTitle>Describe Your Visualization</CardTitle>
            <CardDescription>
              Enter a natural language description of the mathematical concept you'd like to visualize
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <Textarea
              placeholder="e.g., Show me how a Fourier series builds a square wave with 5 terms"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              className="min-h-[100px]"
            />
            <Button 
              onClick={handleGenerate} 
              disabled={!prompt.trim() || isLoading}
              className="w-full"
            >
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Generating Visualization...
                </>
              ) : (
                <>
                  <Play className="mr-2 h-4 w-4" />
                  Generate Visualization
                </>
              )}
            </Button>
          </CardContent>
        </Card>

        {/* Error Display */}
        {error && (
          <Card className="border-red-200 bg-red-50">
            <CardContent className="pt-6">
              <p className="text-red-600">{error}</p>
            </CardContent>
          </Card>
        )}

        {/* Result Section */}
        {result && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                Visualization Result
                <Button onClick={handleDownload} variant="outline" size="sm">
                  <Download className="mr-2 h-4 w-4" />
                  Download
                </Button>
              </CardTitle>
              <CardDescription>
                Visualization Type: {result.visualization_type}
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="bg-gray-50 p-4 rounded-lg">
                <h4 className="font-medium text-sm text-gray-700 mb-2">Refined Prompt:</h4>
                <p className="text-sm text-gray-600">{result.refined_prompt}</p>
              </div>
              
              <div className="aspect-video bg-black rounded-lg overflow-hidden">
                <video
                  src={result.video_url}
                  controls
                  className="w-full h-full"
                  autoPlay
                  loop
                >
                  Your browser does not support the video tag.
                </video>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Examples Section */}
        <Card>
          <CardHeader>
            <CardTitle>Example Prompts</CardTitle>
            <CardDescription>
              Try these example prompts to get started
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {[
                "Show me how a Fourier series builds a square wave",
                "Visualize the transformation of a unit circle under a 2x2 matrix",
                "Animate the convergence of the Taylor series for e^x",
                "Show how eigenvalues affect linear transformations"
              ].map((example, index) => (
                <Button
                  key={index}
                  variant="outline"
                  className="text-left h-auto p-4 justify-start"
                  onClick={() => setPrompt(example)}
                >
                  {example}
                </Button>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
