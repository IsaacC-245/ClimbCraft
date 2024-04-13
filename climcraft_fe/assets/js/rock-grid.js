// Initialize the grids
const grids = {
  "grid-7x10": 70,
  "grid-8x12": 96,
  "grid-12x12": 144,
};

function createCircles(gridClass, count) {
  const container = document.querySelector("." + gridClass);
  container.innerHTML = ""; // Clear previous circles
  for (let i = 0; i < count; i++) {
    const button = document.createElement("button");
    button.className = "circle-button";
    button.addEventListener("click", changeColor);
    container.appendChild(button);
  }
}

function changeColor(event) {
  const button = event.target;
  const colors = ["grey", "green", "yellow", "orange"];
  // Use backgroundColor in RGB format because some browsers return computed color in RGB format
  let currentColor = window.getComputedStyle(button).backgroundColor;
  let currentColorIndex = colors
    .map((color) => `rgb(${getColorComponents(color).join(", ")})`)
    .indexOf(currentColor);
  // Set the next color or default to the first color if not found
  button.style.backgroundColor =
    colors[(currentColorIndex + 1) % colors.length];
}

function getColorComponents(color) {
  const canvas = document.createElement("canvas");
  canvas.width = canvas.height = 1;
  const ctx = canvas.getContext("2d");
  ctx.fillStyle = color;
  ctx.fillRect(0, 0, 1, 1);
  return [...ctx.getImageData(0, 0, 1, 1).data].slice(0, 3);
}

function displayGrid(gridClass, count) {
  // Hide all grids
  Object.keys(grids).forEach((classKey) => {
    const grid = document.querySelector("." + classKey);
    if (grid) grid.classList.add("hidden");
  });

  // Display the selected grid
  const selectedGrid = document.querySelector("." + gridClass);
  if (selectedGrid) {
    selectedGrid.classList.remove("hidden");
    createCircles(gridClass, count);
  }
}

// Initialize the default grid
window.onload = () => {
  displayGrid("grid-7x10", grids["grid-7x10"]);
};
