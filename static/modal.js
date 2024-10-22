
document.addEventListener("DOMContentLoaded", function() {
    // Get modal element
    var modal = document.getElementById("newThreadModal");
    // Get all open modal buttons
    var openModalBtns = document.querySelectorAll(".openModalBtn");
    // Get close button
    var closeBtn = document.getElementsByClassName("closeBtn")[0];

    // Listen for open click on all buttons
    openModalBtns.forEach(function(btn) {
        btn.addEventListener("click", function() {
            modal.style.display = "block";
        });
    });

    // Listen for close click
    closeBtn.addEventListener("click", function() {
        modal.style.display = "none";
    });

    // Listen for outside click
    window.addEventListener("click", function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    });
});