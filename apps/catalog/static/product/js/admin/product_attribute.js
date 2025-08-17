let typeValue;
let currentAttrs;

async function getAttrsFromServer(id) {
  const url = `/api/catalog/admin/attrs/${id ? String(id) + "/" : ""}`;
  const res = await fetch(url, {
    cache: "no-store",
  });
  const attrs = await res.json();
  currentAttrs = attrs;
  return attrs;
}

async function init() {
  const select = document.getElementById("id_type");
  typeValue = select.options[select.selectedIndex].value || undefined;
  const attrs = await getAttrsFromServer(typeValue);
  select.addEventListener("change", handleTypeChange);
  initAttrs();

  setAttrs(attrs);
}

function initAttrs() {
  const attributes = document.getElementById("attributes-group");
  const attributesRows = attributes.querySelectorAll(".form-row");
  for (let i = 0; attributesRows.length > i; i++) {
    const select = attributesRows[i].querySelector(".field-attribute select");
    select.addEventListener("change", handleAttrChange);
  }
  const observer = new MutationObserver(handleNewAttribute);
  observer.observe(attributes.querySelector("tbody"), {
    childList: true,
    subtree: true,
  });
}

function setAttrs(attrsFromServer) {
  const attributes = document.getElementById("attributes-group");
  const attributesRows = attributes.querySelectorAll(".form-row");
  for (let i = 0; attributesRows.length > i; i++) {
    const select = attributesRows[i].querySelector(".field-attribute select");
    const selectedValue = select.options[select.selectedIndex].value;
    for (let i = select.options.length - 1; i > 0; i--) {
      select.options.remove(i);
    }
    for (const a in attrsFromServer) {
      const option = document.createElement("option");
      option.value = attrsFromServer[a].id;
      option.text = attrsFromServer[a].name;
      if (
        selectedValue &&
        Number(attrsFromServer[a].id) === Number(selectedValue)
      ) {
        option.selected = true;
      }
      select.add(option);
    }
    const selectedAttr = attrsFromServer.find(
      (item) => item.id === Number(selectedValue)
    );
    if (!selectedAttr) {
      select.options[0].selected = true;
      select.selectedIndex = 0;
    }

    setAttrValues(Number(selectedValue), attributesRows[i], attrsFromServer);
  }
}

function setAttrValues(selectedAttr, rowElement, attrsFromServer) {
  const select = rowElement.querySelector(".field-value select");
  const selectedValue = select.options[select.selectedIndex].value;
  for (let i = select.options.length - 1; i > 0; i--) {
    select.options.remove(i);
  }
  const selectedAttrObj = attrsFromServer.find(
    (item) => item.id === selectedAttr
  );

  if (!selectedAttrObj) return;

  for (const v of selectedAttrObj.values) {
    const option = document.createElement("option");
    option.value = v.id;
    option.text = v.name;
    if (selectedValue && Number(v.id) === Number(selectedValue)) {
      option.selected = true;
    }
    select.add(option);
  }
}

async function handleTypeChange(e) {
  const attrs = await getAttrsFromServer(e.target.value);
  setAttrs(attrs);
}

function handleAttrChange(e) {
  const selectedAttr = Number(e.target.value);
  const rowElement = e.target.closest(".form-row");
  setAttrValues(selectedAttr, rowElement, currentAttrs);
}

function handleNewAttribute(mutations) {
  for (const mutation of mutations) {
    if (
      mutation.addedNodes[0] &&
      mutation.addedNodes[0].classList.contains("dynamic-attributes")
    ) {
      const newSelect = mutation.addedNodes[0].querySelector(
        ".field-attribute select"
      );
      newSelect.addEventListener("change", handleAttrChange);
    }
  }
}

document.addEventListener("DOMContentLoaded", init, { once: true });
