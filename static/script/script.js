document.addEventListener('DOMContentLoaded', () => {
    let currentPage = 1;
    const totalPages = 4;

    const homeButton = document.getElementById('homeButton');
    const backButton = document.getElementById('backButton');
    const nextButton = document.getElementById('nextButton');
    const pages = document.querySelectorAll('.page');

    // Function to show the current page
    function showPage(pageNumber) {
        pages.forEach((page) => {
            page.classList.remove('active');
        });
        document.getElementById(`page${pageNumber}`).classList.add('active');
        backButton.style.display = (pageNumber === 1) ? 'none' : 'inline-block';
        nextButton.style.display = (pageNumber === totalPages) ? 'none' : 'inline-block';
    }

    homeButton.addEventListener('click', () => {
        currentPage = 1;
        showPage(currentPage);
    });

    backButton.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            showPage(currentPage);
        }
    });

    nextButton.addEventListener('click', () => {
        if (currentPage < totalPages) {
            currentPage++;
            showPage(currentPage);
        }
    });

    showPage(currentPage);
});
