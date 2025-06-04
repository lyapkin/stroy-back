(function () {
  async function handleCategoryChange(e) {
    const attributesGroup = document.getElementById("attributes-group");
    const attributeSelects = attributesGroup.querySelectorAll(
      ".field-attribute select"
    );

    attributeSelects.forEach((item) => {
      for (let i = item.length - 1; i > 0; i--) {
        const r = item.remove(i);
      }
    });

    if (e.target.value) {
      const res = await fetch(
        `/api/catalog/category-attributes/${e.target.value}/`,
        {
          cache: "no-store",
        }
      );
      const data = await res.json();

      attributeSelects.forEach((item) => {
        for (let i = 0; i < data.length; i++) {
          const option = document.createElement("option");
          option.value = data[i][0];
          option.innerText = data[i][1];
          item.append(option);
        }
      });
    }
  }

  const handleLoad = () => {
    const category = document.getElementById("id_category");

    if (category && category.selectedIndex === 0) {
      category.addEventListener("change", handleCategoryChange);
      const attributesGroup = document.getElementById("attributes-group");
      const attributeSelects = attributesGroup.querySelectorAll(
        ".field-attribute select"
      );

      attributeSelects.forEach((item) => {
        for (let i = item.length - 1; i > 0; i--) {
          const r = item.remove(i);
        }
      });
    }
  };

  window.addEventListener("load", handleLoad);
})();
