const textToType = "Hello, I'm Eric.";

// Target the header element
const headerElement = document.getElementById('header-text');

// Typing effect settings
let index = 0;  // Starting index of the text
const typingSpeed = 100;  // Typing speed in milliseconds

// Function to simulate typing effect
function typeText() {
  if (index < textToType.length) {
    headerElement.textContent = textToType.substring(0, index + 1); // Append next character
    index++; // Move to the next character
    setTimeout(typeText, typingSpeed); // Call function again after delay
  }
}

// Call the function to start typing
document.addEventListener('DOMContentLoaded', () => {
  headerElement.textContent = '';
  setTimeout(typeText, typingSpeed);  // Start typing after DOM is fully loaded
});