window.onload = function() {
  const colors = ['#e98a9b', '#A5E3E0', '#F3E5AB','#ACE1AF'];
  const randomColor = colors[Math.floor(Math.random() * colors.length)];
  document.body.style.backgroundColor = randomColor;

  const buttons = document.querySelectorAll('#button1');
  const messageInput = document.querySelector('.message-input input[type="text"]');
  buttons.forEach(function(button) {
    button.style.backgroundColor = darkenColor(randomColor, 0.02);
  });
  messageInput.style.backgroundColor = randomColor;
};

function darkenColor(color, amount) {
  // Convert color to RGB format
  let r = parseInt(color.substring(1, 3), 16);
  let g = parseInt(color.substring(3, 5), 16);
  let b = parseInt(color.substring(5, 7), 16);

  // Apply darkening factor
  r = Math.floor(r * (1 - amount));
  g = Math.floor(g * (1 - amount));
  b = Math.floor(b * (1 - amount));

  // Convert RGB back to hex format
  r = r.toString(16).padStart(2, '0');
  g = g.toString(16).padStart(2, '0');
  b = b.toString(16).padStart(2, '0');
  let darkerColor = `#${r}${g}${b}`;

  return darkerColor;
}

function lightenColor(color, amount) {
  // Convert color to RGB format
  let r = parseInt(color.substring(1, 3), 16);
  let g = parseInt(color.substring(3, 5), 16);
  let b = parseInt(color.substring(5, 7), 16);

  // Apply lightening factor
  r = Math.floor(r + (255 - r) * amount);
  g = Math.floor(g + (255 - g) * amount);
  b = Math.floor(b + (255 - b) * amount);

  // Convert RGB back to hex format
  r = r.toString(16).padStart(2, '0');
  g = g.toString(16).padStart(2, '0');
  b = b.toString(16).padStart(2, '0');
  let lighterColor = `#${r}${g}${b}`;

  return lighterColor;
}

/* Add your JavaScript code here */
const form = document.querySelector('form');
form.addEventListener('submit', (event) => {
  event.preventDefault();
  const searchTerm = form.querySelector('input[type="text"]').value;
  const category = form.querySelector('select').value;
  // Add code to perform search here
});

// Preview uploaded image
const fileInput = document.getElementById("profile_pic");
const previewImg = document.getElementById("preview");
fileInput.addEventListener("change", function() {
  const file = fileInput.files[0];
  const reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onload = function() {
    previewImg.src = reader.result;
    previewImg.style.display = "block";
  }
});