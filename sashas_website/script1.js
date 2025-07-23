document.addEventListener("DOMContentLoaded", () => {
    const togglebtn = document.getElementById("toggle-mode");
    const body = document.body;
    const textBg = document.getElementById("about-text-container");

    togglebtn.addEventListener('click', () =>{
        body.classList.toggle('dark-mode');
        togglebtn.classList.toggle('dark-mode-btn');
        textBg.classList.toggle('dark-mode-about-text');
    });  
});