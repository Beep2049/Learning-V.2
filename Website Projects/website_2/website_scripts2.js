// Pop-Up Window Feature 
document.querySelectorAll('.folder').forEach(folder => {
    folder.addEventListener('click', e => {
        const modalID = folder.dataset.modal;
        const modal = document.getElementById(modalID);

        folder.classList.add('clicked');

        setTimeout(() => {
            folder.classList.remove('clicked');
            modal.classList.remove('modal-hidden');
        }, 100);
    });
});

document.querySelectorAll('.close-btn'). forEach(button => {
    button.addEventListener('click', e => {
        const modal = button.closest('.modal');
        modal.classList.add('modal-hidden');
    });
});


// Window Drag Function
function makeDraggable(modal){
    const header = modal.querySelector('.modal-header');
    let offsetX = 0, offsetY = 0, isDragging = false;

    header.addEventListener('mousedown', (e) => {
        isDragging = true;
        document.body.classList.add('dragging')
        offsetX = e.clientX - modal.offsetLeft;
        offsetY = e.clientY - modal.offsetTop

    });

    document.addEventListener('mouseup', () => {
        isDragging = false;
        document.body.classList.remove('dragging')
    });

    document.addEventListener('mousemove', (e) => {
        if (isDragging) {
            modal.style.left = (e.clientX - offsetX) + 'px';
            modal.style.top = (e.clientY - offsetY) + 'px';
        }
    });
}

document.querySelectorAll('.modal').forEach(makeDraggable);

