const task = document.getElementById("task");
const inputText = document.getElementById("inputText");
const submitBtn = document.getElementById("submitBtn");
const result = document.getElementById("result");


submitBtn.addEventListener("click", async () => {

    const selectedTask = task.value;
    const text = inputText.value.trim();

    if (!text) {
        result.innerHTML = `
            <div class="answer-card">
                Please enter something first.
            </div>
        `;
        return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = "Thinking...";

    result.innerHTML = `
        <div class="loading">
            🤖 EduGenie is preparing your answer...
        </div>
    `;

    try {

        let endpoint;
        let body;

        if (selectedTask === "qa") {

            endpoint = "/qa";

            body = {
                question: text
            };

        } else if (selectedTask === "explain") {

            endpoint = "/explain";

            body = {
                topic: text
            };

        } else if (selectedTask === "quiz") {

            endpoint = "/quiz";

            body = {
                text: text
            };

        } else if (selectedTask === "summarize") {

            endpoint = "/summarize";

            body = {
                text: text
            };

        } else if (selectedTask === "learn") {

            endpoint = "/learn/recommendations";

            body = {
                text: text
            };
        }


        const response = await fetch(endpoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        });


        const responseText = await response.text();

let data;

try {
    data = JSON.parse(responseText);
} catch {
    throw new Error(responseText || "Server error occurred.");
}


        if (!response.ok) {
            throw new Error(data.detail || "Something went wrong.");
        }


        if (selectedTask === "quiz") {

            displayQuiz(data);

        } else {

            displayAnswer(data.answer);

        }

    } catch (error) {

        result.innerHTML = `
            <div class="answer-card">
                <h2>Something went wrong</h2>
                <p>${escapeHtml(error.message)}</p>
            </div>
        `;

    } finally {

        submitBtn.disabled = false;
        submitBtn.textContent = "Ask EduGenie";

    }
});


function displayAnswer(answer) {

    const formattedAnswer = escapeHtml(answer)
        .replace(/^### (.*)$/gm, "<h3>$1</h3>")
        .replace(/^## (.*)$/gm, "<h2>$1</h2>")
        .replace(/^# (.*)$/gm, "<h1>$1</h1>")
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/\n/g, "<br>");

    result.innerHTML = `
        <div class="answer-card">
            ${formattedAnswer}
        </div>
    `;
}


function displayQuiz(data) {

    if (!data.questions || data.questions.length === 0) {

        result.innerHTML = `
            <div class="answer-card">
                No quiz questions were generated.
            </div>
        `;

        return;
    }


    const quizContainer = document.createElement("div");

    quizContainer.className = "quiz-container";


    const title = document.createElement("h2");

    title.className = "quiz-title";
    title.textContent = "Quiz";

    quizContainer.appendChild(title);


    data.questions.forEach((question, questionIndex) => {

        const questionBox = document.createElement("div");

        questionBox.className = "quiz-question";


        const questionText = document.createElement("div");

        questionText.className = "question-text";

        questionText.textContent =
            `${questionIndex + 1}. ${question.question}`;

        questionBox.appendChild(questionText);


        const optionList = document.createElement("div");

        optionList.className = "option-list";


        question.options.forEach((option, optionIndex) => {

            const label = document.createElement("label");

            label.className = "option";


            const radio = document.createElement("input");

            radio.type = "radio";
            radio.name = `question-${questionIndex}`;
            radio.value = option;


            const letter = document.createElement("strong");

            letter.textContent =
                `${String.fromCharCode(65 + optionIndex)}.`;


            const optionText = document.createElement("span");

            optionText.textContent = option;


            label.appendChild(radio);
            label.appendChild(letter);
            label.appendChild(optionText);

            optionList.appendChild(label);
        });


        questionBox.appendChild(optionList);


        const checkButton = document.createElement("button");

        checkButton.className = "check-answer";

        checkButton.textContent = "Check Answer";


        const feedback = document.createElement("div");

        feedback.className = "feedback";


        checkButton.addEventListener("click", () => {

            const selected = questionBox.querySelector(
                `input[name="question-${questionIndex}"]:checked`
            );


            if (!selected) {

                feedback.className = "feedback wrong";

                feedback.textContent =
                    "⚠️ Please select an answer.";

                return;
            }


            const allOptions =
                questionBox.querySelectorAll(".option");


            allOptions.forEach(option => {

                option.classList.remove(
                    "correct-option",
                    "wrong-option"
                );

            });


            if (selected.value === question.answer) {

                feedback.className = "feedback correct";

                feedback.textContent = "✅ Correct!";

                selected.closest(".option")
                    .classList.add("correct-option");

            } else {

                feedback.className = "feedback wrong";

                feedback.textContent =
                    `❌ Incorrect. Correct answer: ${question.answer}`;

                selected.closest(".option")
                    .classList.add("wrong-option");

                allOptions.forEach(option => {

                    const radio = option.querySelector("input");

                    if (radio.value === question.answer) {

                        option.classList.add("correct-option");

                    }
                });
            }
        });


        questionBox.appendChild(checkButton);
        questionBox.appendChild(feedback);

        quizContainer.appendChild(questionBox);

    });


    result.innerHTML = "";

    result.appendChild(quizContainer);
}


function escapeHtml(text) {

    const div = document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}