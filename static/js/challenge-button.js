document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".btn").forEach(button => {
        button.addEventListener("click", function() {
            window.location.href = this.getAttribute("data-url");
        });
    });
});
