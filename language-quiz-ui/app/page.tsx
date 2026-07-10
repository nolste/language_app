"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { startQuiz } from "@/lib/api"

export default function Home() {
  const router = useRouter()
  const [loading, setLoading] = useState(false)

  const userId = "00000000-0000-0000-0000-000000000001" // temp dev user

  async function handleStart() {
    setLoading(true)

    const data = await startQuiz(userId, 10)

    router.push(`/quiz/${data.session_id}`)
  }

  return (
    <div className="flex flex-col items-center justify-center h-screen gap-4">
      <h1 className="text-2xl font-bold">Portuguese Quiz</h1>

      <button
        onClick={handleStart}
        disabled={loading}
        className="px-4 py-2 bg-blue-600 text-white rounded"
      >
        {loading ? "Starting..." : "Start Quiz"}
      </button>
    </div>
  )
}