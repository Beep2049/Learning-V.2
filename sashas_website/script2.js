document.addEventListener("DOMContentLoaded", () => {
    const track = document.getElementById("belt-track");
    const leftArrow = document.getElementById("arrow-left");
    const rightArrow = document.getElementById("arrow-right");
    const slides = document.querySelectorAll(".pastry-slide");
    let scrollInterval;
    let isUserInteracting = false;

    //Scroll function, to the left
    function scrollBelt(direction){
        track.scrollBy({ left: direction * 300, behavior: "smooth"});
    }

    //Auto Scroll function
    function autoScroll(){
        if(!isUserInteracting){
            scrollBelt(1);
        }
    }
    
    //Idle timeout function, if no activity happens for a certain amount of time
    let idleTimeout;
    function resetIdleTimer(){
        isUserInteracting = true;
        clearTimeout(idleTimeout);
        idleTimeout = setTimeout(()=>{
            isUserInteracting = false;
        }, 5000);
    }

    //Left arrow click resets the idle timer
    leftArrow.addEventListener('click', () =>{
        scrollBelt(-1);
        resetIdleTimer();
    })

    //Right arrow click resets the idle timer
    rightArrow.addEventListener('click', () =>{
        scrollBelt(1);
        resetIdleTimer();
    })

    //Infinite Looping Scroll
    track.addEventListener('scroll', () =>{
        const maxScrollLeft = track.scrollWidth - track.clientWidth;
        if(track.scrollLeft >= maxScrollLeft){
            track.scrollTo({left: 0, behavior: 'smooth'});
        }
    });

    //Autoscroll every three seconds
    scrollInterval = setInterval(autoScroll, 5000);

    
    //Pop-Up Script//


    //Popup behavior
    const modal = document.getElementById("popup-modal");
    const modalImg = document.getElementById("popup-image");
    const closeBtn = document.querySelector('.close-btn');

    slides.forEach(slide =>{
        slide.addEventListener('click', () => {
            modal.style.display = 'block';
            modalImg.src = slide.querySelector('img').src;
        });
    });

    closeBtn.onclick = () => (modal.style.display = 'none');
    window.onclick = event =>{
        if(event.target === modal) modal.style.display = 'none';
    }
})