const sidebar = document.querySelector(".page-sidebar");
const sidebarBtn = document.querySelector(".ps-toggle");

sidebarBtn.addEventListener("click", () => {
    sidebar.classList.toggle("active");
})