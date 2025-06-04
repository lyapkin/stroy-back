const unmaskNumber = (value) => {
  return value.replace(/\D/g, "");
};

const handleLoad = () => {
  const phoneInputs = document.querySelectorAll("input[type=tel]");

  const onChange = (e) => {
    const dirtyValue = e.target.value;
    const cleanValue = unmaskNumber(dirtyValue);

    let result = "";

    if (dirtyValue[0] === "7" || dirtyValue[0] === "8") {
      result = "+7" + cleanValue.slice(1);
    } else if (dirtyValue[0] !== "+" && dirtyValue !== "") {
      result = "+7" + cleanValue;
    } else if (dirtyValue[0] === "+") {
      result = "+" + cleanValue;
    }

    if (result.length > 2 && result.startsWith("+7")) {
      result = result.slice(0, 2) + " (" + result.slice(2);
    }
    if (result.length > 7 && result.startsWith("+7")) {
      result = result.slice(0, 7) + ") " + result.slice(7);
    }
    if (result.length > 12 && result.startsWith("+7")) {
      result = result.slice(0, 12) + "-" + result.slice(12);
    }
    if (result.length > 15 && result.startsWith("+7")) {
      result = result.slice(0, 15) + "-" + result.slice(15);
    }

    if (result.startsWith("+7")) {
      result = result.slice(0, 18);
    } else {
      result = result.slice(0, 16);
    }

    e.target.value = result;
  };

  for (const input of phoneInputs) {
    input.addEventListener("input", onChange);
  }

  const content = document.getElementById("content-main");
  const observer = new MutationObserver((mutations) => {
    for (const mutation of mutations) {
      if (
        mutation.addedNodes[0] &&
        mutation.addedNodes[0].classList.contains("dynamic-phones")
      ) {
        mutation.addedNodes[0].children[2].children[0].addEventListener(
          "input",
          onChange
        );
      }

      if (
        mutation.removedNodes[0] &&
        mutation.removedNodes[0].classList.contains("dynamic-phones")
      ) {
        mutation.removedNodes[0].children[2].children[0].removeEventListener(
          "input",
          onChange
        );
      }
    }
  });
  observer.observe(content, { childList: true, subtree: true });
};

window.addEventListener("load", handleLoad);
