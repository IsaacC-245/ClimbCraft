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
    // Assign a unique ID based on the grid class and index
    button.id = `${gridClass}-button-${i}`;
    button.addEventListener("click", changeColor);
    container.appendChild(button);
  }
}

function changeColor(event) {
  const button = event.target;
  const colors = ["#d3d3d3", "#a3ffb4", "#fef65b", "#ffa500"];
  let currentColor = window.getComputedStyle(button).backgroundColor;
  let currentColorIndex = colors
    .map((color) => `rgb(${getColorComponents(color).join(", ")})`)
    .indexOf(currentColor);
  const nextColor = colors[(currentColorIndex + 1) % colors.length];
  button.style.backgroundColor = nextColor;

  // Example of sending the updated state to the server
  saveButtonState(button.id, nextColor);
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
    selectedGrid.setAttribute("id", "route_grid")
    createCircles(gridClass, count);
  }
}

// Initialize the default grid
window.onload = () => {
  displayGrid("grid-12x12", grids["grid-12x12"]);
};

// Save button state functions

function submitButton() {
  var tempString = "";
  var stringList = [];
  var count = 0;
  let grid_container = document.getElementById("route_grid").children; // Ensure you are looping through the children of the grid
  for(let grid_child of grid_container){ // Changed to a proper for...of loop
    if(grid_child.nodeType === 1){ // Check if the element is an actual DOM element
      if(count == 11){
          tempString += grid_child.textContent.trim() + " "; // Collecting text content from children
          stringList.push(tempString.trim());
          tempString = "";
          count = 0;
      } else {
          tempString += grid_child.textContent.trim() + " ";
          count++;
      }
    }
  }
  if(tempString !== "") stringList.push(tempString.trim()); // Push any remaining string if not empty
  return stringList;
}

// Event listeners for the buttons
document.getElementById('save-button').addEventListener('click', function() {
  console.log('Save pressed');
  let data = submitButton();
  console.log(data); // Log the data or process it
});

document.getElementById('save-close-button').addEventListener('click', function() {
  console.log('Save & Close pressed');
  let data = submitButton();
  console.log(data); // Log the data or process it
  window.close(); // Close the window or tab, adjust according to your app's needs
});

document.getElementById('close-button').addEventListener('click', function() {
  console.log('Close pressed');
  window.close(); // Close the window or tab, adjust according to your app's needs
});