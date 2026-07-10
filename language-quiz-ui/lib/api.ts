const BASE_URL = "http://localhost:8000"

export async function startQuiz(user_id: string, num_questions = 10) {
    const res = await fetch(`${BASE_URL}/quiz/start`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id, num_questions }),
    })

    return res.json()
}

export async function submitQuiz(payload: {
    session_id: string
    answers: Record<string, string>
}) {
    const res = await fetch(`${BASE_URL}/quiz/submit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    })

    return res.json()
}