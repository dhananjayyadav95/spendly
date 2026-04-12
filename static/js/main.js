// main.js — students will add JavaScript here as features are built

(function() {
    'use strict';

    const modal = document.getElementById('videoModal');
    const modalTrigger = document.getElementById('modalTrigger');
    const modalClose = modal ? modal.querySelector('.modal-close') : null;
    const videoFrame = document.getElementById('videoFrame');
    const originalVideoSrc = videoFrame ? videoFrame.src : '';

    function openModal() {
        if (modal && videoFrame) {
            videoFrame.src = originalVideoSrc;
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
    }

    function closeModal() {
        if (modal && videoFrame) {
            modal.classList.remove('active');
            document.body.style.overflow = '';
            videoFrame.src = '';
        }
    }

    if (modalTrigger) {
        modalTrigger.addEventListener('click', openModal);
    }

    if (modalClose) {
        modalClose.addEventListener('click', closeModal);
    }

    if (modal) {
        modal.addEventListener('click', function(event) {
            if (event.target === modal) {
                closeModal();
            }
        });
    }

    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && modal && modal.classList.contains('active')) {
            closeModal();
        }
    });
})();
