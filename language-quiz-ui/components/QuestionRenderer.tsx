type Props = {
    question: any
    value: any
    onChange: (val: any) => void
}

export default function QuestionRenderer({
    question,
    value,
    onChange,
}: Props) {
    console.log("QUESTION:", question)
    console.log("CHOICES:", question?.choices)

    switch (question.question_type) {
        case "multiple_choice":
            return (
                <div className="space-y-2">
                    <p className="text-lg">{question.prompt}</p>

                    <div className="flex flex-col gap-2">
                        {question.choices?.map((c: string) => (
                            <button
                                key={c}
                                onClick={() => onChange(c)}
                                className={`p-2 border rounded ${value === c ? "bg-blue-200" : ""
                                    }`}
                            >
                                {c}
                            </button>
                        ))}
                    </div>
                </div>
            )

        case "fill_blank":
            return (
                <div className="space-y-2">
                    <p className="text-lg">{question.prompt}</p>

                    <input
                        className="border p-2 w-full"
                        value={value || ""}
                        onChange={(e) => onChange(e.target.value)}
                    />

                    {question.hint && (
                        <p className="text-sm text-gray-500">
                            Hint: {question.hint}
                        </p>
                    )}
                </div>
            )

        case "translation":
        case "error_correction":
            return (
                <div className="space-y-2">
                    <p className="text-lg">{question.prompt}</p>

                    <textarea
                        className="border p-2 w-full"
                        value={value || ""}
                        onChange={(e) => onChange(e.target.value)}
                    />
                </div>
            )

        default:
            return <div>Unknown type</div>

    }

}