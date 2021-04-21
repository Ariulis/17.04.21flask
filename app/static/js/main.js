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

addPostButton.addEventListener("click", function () {
  this.style.display = "none";
  postForm.style.display = "block";
});

preloader
  .querySelector(".spinner-border")
  .classList.add(`text-${bootstrapColors[Math.floor(Math.random() * 8)]}`);

document.addEventListener("DOMContentLoaded", function () {
  setTimeout(() => (preloader.style.display = "none"), 600);
});
