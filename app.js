window.onload = function() {
  const colors = ['#99e999', '#e98a9b', '#A5E3E0', '#E9EC6B'];
  const randomColor = colors[Math.floor(Math.random() * colors.length)];
  document.body.style.backgroundColor = randomColor;
};