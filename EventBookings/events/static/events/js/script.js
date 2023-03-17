"use strict";
const events = document.querySelectorAll(".events");

// Forms Close Buttons
const formCloseBtns = document.querySelectorAll(".close");

formCloseBtns.forEach((btn) =>
  btn.addEventListener("click", (e) => {
    e.target.parentElement.classList.add("hide");
  })
);

// Edit Page: Add Forms
const addSelectBtns = document.querySelectorAll(".add-menu button");
const addForms = document.querySelectorAll(".add-form");

addSelectBtns.forEach((btn) =>
  btn.addEventListener("click", (e) => {
    addForms.forEach((form) => {
      form.classList.add("hide");
      if (form.id === e.target.value.toLowerCase()) {
        form.classList.remove("hide");
      }
    });
  })
);

// Profile Page: Edit Profile Details
const profileSelectBtns = document.querySelectorAll(".profile-menu button");
const profileEditForm = document.getElementById("profile-edit");

profileSelectBtns.forEach((btn) =>
  btn.addEventListener("click", (e) => {
    profileEditForm.classList.remove("hide");
  })
);

// Date Picker
const elems = document.querySelectorAll(".datepicker_input");

const getDatePickerTitle = (elem) => {
  // From the label or the aria-label
  const label = elem.nextElementSibling;
  let titleText = "";
  if (label && label.tagName === "LABEL") {
    titleText = label.textContent;
  } else {
    titleText = elem.getAttribute("aria-label") || "";
  }
  return titleText;
};

for (const elem of elems) {
  const datepicker = new Datepicker(elem, {
    format: "dd/mm/yyyy", // UK format
    title: getDatePickerTitle(elem),
  });
}

// Filtering Events
const catDropdown = document.querySelector(".cat-dropdown");
const subCatDropdown = document.querySelector(".subCat-dropdown");
const dateField = document.querySelector(".datepicker_input");

catDropdown.onchange = (e) => {
  const date = dateField.value;
  const subCat = subCatDropdown.value.replace(/\s+/g, "");

  events.forEach((event) => event.parentElement.classList.remove("hide"));
  events.forEach((event) => {
    if (date === "" && subCat === "all") {
      if (!event.parentElement.classList.contains(e.target.value))
        event.parentElement.classList.add("hide");
    } else if (date !== "" && subCat === "all") {
      if (
        !(
          event.parentElement.classList.contains(e.target.value) &&
          event.parentElement.classList.contains(date)
        )
      )
        event.parentElement.classList.add("hide");
    } else if (date === "" && subCat !== "all") {
      if (
        !(
          event.parentElement.classList.contains(e.target.value) &&
          event.parentElement.classList.contains(subCat)
        )
      )
        event.parentElement.classList.add("hide");
    } else {
      if (
        !(
          event.parentElement.classList.contains(e.target.value) &&
          event.parentElement.classList.contains(subCat) &&
          event.parentElement.classList.contains(date)
        )
      )
        event.parentElement.classList.add("hide");
    }
  });
};

subCatDropdown.onchange = (e) => {
  const date = dateField.value;
  const cat = catDropdown.value;

  events.forEach((event) => event.parentElement.classList.remove("hide"));
  events.forEach((event) => {
    if (date === "" && cat === "all") {
      if (
        !event.parentElement.classList.contains(
          e.target.value.replace(/\s+/g, "")
        )
      )
        event.parentElement.classList.add("hide");
    } else if (date === "" && cat !== "all") {
      if (
        !(
          event.parentElement.classList.contains(
            e.target.value.replace(/\s+/g, "")
          ) && event.parentElement.classList.contains(cat)
        )
      )
        event.parentElement.classList.add("hide");
    } else if (cat === "all" && date !== "") {
      if (
        !(
          event.parentElement.classList.contains(
            e.target.value.replace(/\s+/g, "")
          ) && event.parentElement.classList.contains(date)
        )
      )
        event.parentElement.classList.add("hide");
    } else {
      if (
        !(
          event.parentElement.classList.contains(
            e.target.value.replace(/\s+/g, "")
          ) &&
          event.parentElement.classList.contains(cat) &&
          event.parentElement.classList.contains(date)
        )
      )
        event.parentElement.classList.add("hide");
    }
  });
};

dateField.addEventListener("changeDate", (e) => {
  const subCat = subCatDropdown.value.replace(/\s+/g, "");
  const cat = catDropdown.value;

  events.forEach((event) => event.parentElement.classList.remove("hide"));
  events.forEach((event) => {
    if (e.target.value === "") {
      if (subCat === "all" && cat === "all") {
        event.parentElement.classList.remove("hide");
      } else if (subCat === "all" && cat !== "all") {
        if (!event.parentElement.classList.contains(cat))
          event.parentElement.classList.add("hide");
      } else if (cat === "all" && subCat !== "all") {
        if (!event.parentElement.classList.contains(subCat))
          event.parentElement.classList.add("hide");
      } else {
        if (
          !(
            event.parentElement.classList.contains(subCat) &&
            event.parentElement.classList.contains(cat)
          )
        )
          event.parentElement.classList.add("hide");
      }
    } else {
      if (subCat === "all" && cat === "all") {
        if (!event.parentElement.classList.contains(e.target.value))
          event.parentElement.classList.add("hide");
      } else if (subCat === "all" && cat !== "all") {
        if (
          !(
            event.parentElement.classList.contains(e.target.value) &&
            event.parentElement.classList.contains(cat)
          )
        )
          event.parentElement.classList.add("hide");
      } else if (cat === "all" && subCat !== "all") {
        if (
          !(
            event.parentElement.classList.contains(e.target.value) &&
            event.parentElement.classList.contains(subCat)
          )
        )
          event.parentElement.classList.add("hide");
      } else {
        if (
          !(
            event.parentElement.classList.contains(e.target.value) &&
            event.parentElement.classList.contains(subCat) &&
            event.parentElement.classList.contains(cat)
          )
        )
          event.parentElement.classList.add("hide");
      }
    }
  });
});

// Selected Event Card
const eventCards = document.querySelectorAll(".card");

events.forEach((event) =>
  event.addEventListener("click", (e) =>
    eventCards.forEach((card) => {
      card.scrollIntoView();
      card.classList.add("hide");
      let eventTitle = e.target.parentElement.children[0].innerHTML
        .split(",")[0]
        .replace(/\s+/g, "");
      if (card.classList.contains(eventTitle)) card.classList.remove("hide");
    })
  )
);

// Likes
const toggleHeart = function (img) {
  const heartFill = " ../static/svgIcons/heart-fill.svg";
  const heartEmpty = "../static/svgIcons/heart.svg";

  let btn = img.parentElement;
  console;

  if (btn.classList.contains("fill")) {
    img.src = heartFill;
    btn.classList.remove("fill");
  } else {
    btn.classList.add("fill");
    img.src = heartEmpty;
  }
};

const likeBtn = document.querySelector(".like");

likeBtn.addEventListener("click", (e) => {
  if (e.target.tagName === "IMG") toggleHeart(e.target);
});

//payment
const paymentForm = document.getElementById('payment-form');
const paymentStatus = document.querySelector('.payment-status');

paymentForm.addEventListener('submit', (event) => {
  event.preventDefault();

  const cardNumber = document.getElementById('card-number').value;
  const expirationDate = document.getElementById('expiration-date').value;
  const securityCode = document.getElementById('security-code').value;
  const name = document.getElementById('name').value;

  if (cardNumber.trim() !== '' && expirationDate.trim() !== '' && securityCode.trim() !== '' && name.trim() !== '') {
    // Simulate a delay in payment processing
    setTimeout(() => {
      // Show the payment status message
      paymentStatus.classList.remove('hidden');
    }, 2000);
  } else {
    alert('Please fill in all the required fields.');
  }
});


//chartss
