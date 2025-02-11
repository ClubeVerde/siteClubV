var swiper = new Swiper(".mySwiper", {
    slidesPerView: 3, // Quantidade de itens visíveis
    spaceBetween: 20,
    loop: true,
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    breakpoints: {
        768: { slidesPerView: 2 },
        480: { slidesPerView: 1 }
    }
});
