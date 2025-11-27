// main.js
const buttons = document.querySelectorAll(".accordion-toggle");

buttons.forEach((button) => {
  button.addEventListener("click", () => {
    const content = button.nextElementSibling;
    content.classList.toggle("hidden");

    buttons.forEach((other) => {
      if (other !== button) {
        const otherContent = other.nextElementSibling;
        otherContent.classList.add("hidden");
      }
    });
  });
});