const preloader = document.querySelector(".page-preloader");
const bootstrapColors = [
  "primary",
  "danger",
  "warning",
  "success",
  "info",
  "secondary",
  "light",
  "dark",
];
const postForm = document.querySelector(".index-page .form");
const addPostButton = document.querySelector(".add-post-btn");

if (addPostButton) {
  addPostButton.addEventListener("click", function () {
    if (this.innerText === "Add a post") {
      this.innerText = "Cancel";
      postForm.style.display = "block";
    } else {
      this.innerText = "Add a post";
      postForm.style.display = "none";
    }
  });
}

preloader
  .querySelector(".spinner-border")
  .classList.add(`text-${bootstrapColors[Math.floor(Math.random() * 8)]}`);

document.addEventListener("DOMContentLoaded", function () {
  setTimeout(() => (preloader.style.display = "none"), 600);
});
