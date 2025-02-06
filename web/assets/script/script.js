// Initialize TOC bot with unordered list (ul)
tocbot.init({
  tocSelector: "#toc-container",
  contentSelector: "body",
  headingSelector: "h1, h2, h3, h4, h5, h6",
  // Customize list style
  orderedList: false, // This ensures the TOC is in an unordered list (ul)
});

// Listen for Alt + S to toggle the sidebar visibility
document.addEventListener("keydown", function (event) {
  if (event.altKey && event.key === "s") {
    const sidebar = document.getElementById("sidebar");
    if (sidebar.style.display === "none" || sidebar.style.display === "") {
      sidebar.style.display = "block"; // Show sidebar
    } else {
      sidebar.style.display = "none"; // Hide sidebar
    }
  }
});
