(function () {
  async function handleAttributeChange(e) {
    const attributeValueSelects = e.target
      .closest("tr")
      .querySelectorAll(".field-value select");

    attributeValueSelects.forEach((item) => {
      for (let i = item.length - 1; i > 0; i--) {
        const r = item.remove(i);
      }
    });

    if (e.target.value) {
      const res = await fetch(
        `/api/catalog/attribute-values/${e.target.value}/`,
        {
          cache: "no-store",
        }
      );
      const data = await res.json();

      attributeValueSelects.forEach((item) => {
        for (let i = 0; i < data.length; i++) {
          const option = document.createElement("option");
          option.value = data[i][0];
          option.innerText = data[i][1];
          item.append(option);
        }
      });
    }
  }

  function handleCategoryChange(e) {
    const attributesGroup = document.getElementById("attributes-group");
    const attributeValueSelects = attributesGroup.querySelectorAll(
      ".field-value select"
    );

    attributeValueSelects.forEach((item) => {
      for (let i = item.length - 1; i > 0; i--) {
        const r = item.remove(i);
      }
    });
  }

  function handleLoad() {
    const category = document.getElementById("id_category");

    const attributesGroup = document.getElementById("attributes-group");
    const attributeSelects = attributesGroup.querySelectorAll(
      ".field-attribute select"
    );
    attributeSelects.forEach((item) => {
      item.addEventListener("change", handleAttributeChange);
    });

    if (category && category.selectedIndex === 0) {
      category.addEventListener("change", handleCategoryChange);
    } else {
      attributeSelects.forEach(async (item) => {
        const attributeValueSelects = item
          .closest("tr")
          .querySelectorAll(".field-value select");

        if (!item.value) {
          attributeValueSelects.forEach((item) => {
            for (let i = item.length - 1; i > 0; i--) {
              const r = item.remove(i);
            }
          });
          return;
        }

        let selectedValue;
        attributeValueSelects.forEach((item) => {
          for (let i = item.length - 1; i > 0; i--) {
            if (item[i].selected) {
              selectedValue = item[i].value;
            }
            item.remove(i);
          }
        });

        const res = await fetch(
          `/api/catalog/attribute-values/${item.value}/`,
          {
            cache: "no-store",
          }
        );
        const data = await res.json();
        attributeValueSelects.forEach((item) => {
          for (let i = 0; i < data.length; i++) {
            const option = document.createElement("option");
            option.value = data[i][0];
            option.innerText = data[i][1];
            if (data[i][0] == selectedValue) {
              option.selected = true;
            }
            item.append(option);
          }
        });
      });
    }
  }

  window.addEventListener("load", handleLoad);
})();
