document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("generateButton").addEventListener("click", generateClass);
});

function generateClass() {
  const jsonInput = document.getElementById("jsonInput").value;
  const className = document.getElementById("className").value;
  const caseStyle = document.querySelector('input[name="caseStyle"]:checked')?.value;
  const language = document.getElementById("languageSelect").value;
  const output = document.getElementById("output");

  if (!jsonInput || !caseStyle) {
    output.value = "Please enter JSON and select a case style.";
    return;
  }

  if (!className){
    output.value = "Invalid class name";
  }

  let jsonObj;
  try {
    jsonObj = JSON.parse(jsonInput);
  } catch (e) {
    output.value = "Invalid JSON format.";
    return;
  }

  // call to generate_class endpoint
  fetch("/generate_class", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      json_input: jsonObj,
      class_name: className,
      case_style: caseStyle,
      language: language
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.error) {
      output.value = data.error;
    } else {
      output.value = data.class_output;
    }
  })
  .catch(error => {
    output.value = "An error occurred while generating the class.";
    console.error("Error:", error);
  });
}
