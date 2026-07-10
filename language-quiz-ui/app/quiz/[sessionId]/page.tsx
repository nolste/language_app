"use client"

import { useEffect, useState } from "react"
import { useParams } from "next/navigation"
import QuestionRenderer from "@/components/QuestionRenderer"
import { submitQuiz } from "@/lib/api"

export default function QuizPage() {
    const { sessionId } = useParams()

    const [questions, setQuestions] = useState<any[]>([])
    const [index, setIndex] = useState(0)
    const [answers, setAnswers] = useState<Record<string, any>>({})
    const [results, setResults] = useState<any>(null)

    useEffect(() => {
        const stored = sessionStorage.getItem("quiz")

        if (stored) {
            setQuestions(JSON.parse(stored))
        } else {
            fetch(`http://localhost:8000/quiz/start`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    user_id: "00000000-0000-0000-0000-000000000001",
                    num_questions: 10,
                }),
            })
                .then((r) => r.json())
                .then((data) => {
                    setQuestions(data.questions)
                    sessionStorage.setItem(
                        "quiz",
                        JSON.stringify(data.questions)
                    )
                })
        }
    }, [])

    const question = questions[index]

    function setAnswer(val: any) {
        setAnswers({
            ...answers,
            [question.id]: val,
        })
    }

    async function submit() {
        const res = await submitQuiz({
            session_id: sessionId as string,
            answers,
        })

        setResults(res)
    }

    if (!question) return <div>Loading...</div>

    if (results) {
        return (
            <div className="p-6 space-y-4">
                <h1 className="text-2xl font-bold">Results</h1>
                <p>Total Score: {results.total_score}</p>

                <pre>{JSON.stringify(results.results, null, 2)}</pre>
            </div>
        )
    }

    return (
        <div className="p-6 space-y-4">
            <div>
                Question {index + 1} / {questions.length}
            </div>

            <QuestionRenderer
                question={question}
                value={answers[question.id]}
                onChange={setAnswer}
            />

            <div className="flex gap-2">
                {index > 0 && (
                    <button
                        onClick={() => setIndex(index - 1)}
                        className="px-4 py-2 border"
                    >
                        Back
                    </button>
                )}

                {index < questions.length - 1 ? (
                    <button
                        onClick={() => setIndex(index + 1)}
                        className="px-4 py-2 bg-blue-600 text-white"
                    >
                        Next
                    </button>
                ) : (
                    <button
                        onClick={submit}
                        className="px-4 py-2 bg-green-600 text-white"
                    >
                        Submit
                    </button>
                )}
            </div>
        </div>
    )
}