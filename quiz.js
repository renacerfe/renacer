(() => {
  "use strict";

  let questions = [];
  let currentQuestion = 0;
  let correctCount = 0;
  let incorrectCount = 0;
  let answering = false;

  const quizTitle = document.getElementById("quizTitle");
  const quiz = document.getElementById("quiz");
  const questionText = document.getElementById("questionText");
  const result = document.getElementById("result");
  const gameOver = document.getElementById("gameOver");
  const answerButtons = [...document.querySelectorAll("[data-answer]")];

  function setAnswerButtonsDisabled(disabled) {
    answerButtons.forEach((button) => {
      button.disabled = disabled;
    });
  }

  async function loadQuestions() {
    try {
      const response = await fetch("numeros11.json");
      if (!response.ok) {
        throw new Error(`No se pudo cargar el cuestionario (${response.status})`);
      }

      const data = await response.json();
      if (!Array.isArray(data.preguntas) || data.preguntas.length === 0) {
        throw new Error("El cuestionario no contiene preguntas");
      }

      quizTitle.textContent = data.titulo || "Juegos bíblicos";
      questions = data.preguntas;
      loadQuestion();
    } catch (error) {
      quizTitle.textContent = "No se pudo cargar el juego";
      questionText.textContent = "Comprueba que estés usando un servidor local y que numeros11.json exista.";
      result.textContent = error.message;
      setAnswerButtonsDisabled(true);
    }
  }

  function loadQuestion() {
    if (currentQuestion >= questions.length) {
      endGame();
      return;
    }

    answering = false;
    setAnswerButtonsDisabled(false);
    const question = questions[currentQuestion];
    questionText.textContent = `${question.numero}. ${question.pregunta}`;
    result.textContent = "";
    result.className = "result";
  }

  function checkAnswer(userAnswer) {
    if (answering || !questions[currentQuestion]) {
      return;
    }

    answering = true;
    setAnswerButtonsDisabled(true);
    const correctAnswer = questions[currentQuestion].respuesta;

    if (userAnswer === correctAnswer) {
      correctCount += 1;
      result.textContent = "✅ Correcto";
      result.className = "result result-success";
    } else {
      incorrectCount += 1;
      result.textContent = `❌ Incorrecto. La respuesta correcta es: ${correctAnswer ? "Verdadero" : "Falso"}`;
      result.className = "result result-error";
    }

    window.setTimeout(() => {
      currentQuestion += 1;
      loadQuestion();
    }, 1200);
  }

  function endGame() {
    quiz.hidden = true;
    gameOver.hidden = false;
    document.getElementById("correctCount").textContent = correctCount;
    document.getElementById("incorrectCount").textContent = incorrectCount;
    document.getElementById("total").textContent = questions.length;
  }

  function restartQuiz() {
    currentQuestion = 0;
    correctCount = 0;
    incorrectCount = 0;
    gameOver.hidden = true;
    quiz.hidden = false;
    loadQuestion();
  }

  answerButtons.forEach((button) => {
    button.addEventListener("click", () => {
      checkAnswer(button.dataset.answer === "true");
    });
  });

  document.getElementById("restartQuiz").addEventListener("click", restartQuiz);
  loadQuestions();
})();
