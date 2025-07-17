const display = document.getElementById('display');
const buttons = document.querySelectorAll('.btn');
let currentInput = '0';
let operator = '';
let firstValue = '';
let waitingForSecondValue = false;

buttons.forEach(button => {
  button.addEventListener('click', () => {
    const value = button.textContent;

    if (button.id === 'clear') {
      currentInput = '0';
      operator = '';
      firstValue = '';
      waitingForSecondValue = false;
    } else if (button.classList.contains('operator')) {
      operator = value;
      firstValue = currentInput;
      waitingForSecondValue = true;
    } else if (button.classList.contains('equals')) {
      if (operator && firstValue) {
        currentInput = calculate(firstValue, currentInput, operator);
        operator = '';
        waitingForSecondValue = false;
      }
    } else {
      if (waitingForSecondValue) {
        currentInput = value;
        waitingForSecondValue = false;
      } else {
        currentInput = currentInput === '0' ? value : currentInput + value;
      }
    }

    display.textContent = currentInput;
  });
});

function calculate(first, second, operator) {
  const a = parseFloat(first);
  const b = parseFloat(second);
  if (operator === '+') return (a + b).toString();
  if (operator === '-') return (a - b).toString();
  if (operator === '*') return (a * b).toString();
  if (operator === '/') return b !== 0 ? (a / b).toString() : 'Error';
}
