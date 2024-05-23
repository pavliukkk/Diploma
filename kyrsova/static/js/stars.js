document.addEventListener('DOMContentLoaded', function() {
  const starsContainers = document.querySelectorAll('.rating');

  starsContainers.forEach(function(container) {
    const stars = container.querySelectorAll('.star');
    const ratingValueElement = container.querySelector('.rating-value');
    let ratingValue = ratingValueElement ? parseFloat(ratingValueElement.textContent) : 0;
    let lastRatingValue = ratingValue;

    function setRating(rating) {
      ratingValue = rating;

      stars.forEach(function(star, index) {
        if (index < Math.floor(rating)) {
          star.classList.add('active');
        } else {
          star.classList.remove('active');
        }

        const remainder = rating - Math.floor(rating);
        if (index === Math.floor(rating) && remainder > 0) {
          star.classList.add('partial-star');
          star.style.setProperty('--rating', remainder);
        } else {
          star.classList.remove('partial-star');
          star.style.removeProperty('--rating');
        }
      });
    }

    setRating(ratingValue);

    stars.forEach(function(star, index) {
      star.addEventListener('mouseenter', function() {
        setRating(index + 1);
      });

      star.addEventListener('mouseleave', function() {
        setRating(lastRatingValue);
      });

      star.addEventListener('click', function() {
        lastRatingValue = index + 1;
        ratingValue = lastRatingValue;
      });
    });

    container.addEventListener('mouseleave', function() {
      setRating(lastRatingValue);
    });
  });
});
