document.addEventListener("DOMContentLoaded", function() {
    const portfolioList = document.querySelector(".portfolio__list-img");
    const wrapper = portfolioList.querySelector(".portfolio__wrapper");
    const wrapperMiddle = portfolioList.querySelector(".portfolio__wrapper-middle");
    const wrapperSmall = portfolioList.querySelector(".portfolio__wrapper-small");
    const description = portfolioList.querySelector(".portfolio__name-meal.description");

    let activeItem = null;

    portfolioList.addEventListener("mouseover", function(event) {
        const item = event.target.closest(".portfolio__item-img");
        if (!item) return;

        const itemWrapper = item.querySelector(".portfolio__wrapper");
        const itemWrapperMiddle = item.querySelector(".portfolio__wrapper-middle");
        const itemWrapperSmall = item.querySelector(".portfolio__wrapper-small");
        const itemDescription = item.querySelector(".portfolio__name-meal.description");

        if (itemWrapper) {
            const descriptionHeight = itemDescription.clientHeight;
            itemWrapper.style.transition = "transform 0.5s ease-in-out, margin-top 0.5s ease-in-out";
            itemWrapper.style.transform = `translateY(-${descriptionHeight + 20}px)`;
            itemWrapper.style.marginTop = `${descriptionHeight}px`;
        }

        if (itemWrapperMiddle) {
            const descriptionHeight = itemDescription.clientHeight;
            itemWrapperMiddle.style.transition = "transform 0.5s ease-in-out, margin-top 0.5s ease-in-out";
            itemWrapperMiddle.style.transform = `translateY(-${descriptionHeight + 20}px)`;
            itemWrapperMiddle.style.marginTop = `${descriptionHeight}px`;
        }

        if (itemWrapperSmall) {
            const descriptionHeight = itemDescription.clientHeight;
            itemWrapperSmall.style.transition = "transform 0.5s ease-in-out, margin-top 0.5s ease-in-out";
            itemWrapperSmall.style.transform = `translateY(-${descriptionHeight + 20}px)`;
            itemWrapperSmall.style.marginTop = `${descriptionHeight}px`;
        }

        setTimeout(function() {
            if (itemDescription) {
                itemDescription.style.transition = "opacity 0.6s ease-in-out";
                itemDescription.style.opacity = "1";
            }
        }, 500); // Час затримки для появлення тексту (500 мс)

        activeItem = item;
    });

    portfolioList.addEventListener("mouseout", function(event) {
        if (activeItem && !activeItem.contains(event.relatedTarget)) {
            const itemWrapper = activeItem.querySelector(".portfolio__wrapper");
            const itemWrapperMiddle = activeItem.querySelector(".portfolio__wrapper-middle");
            const itemWrapperSmall = activeItem.querySelector(".portfolio__wrapper-small");
            const itemDescription = activeItem.querySelector(".portfolio__name-meal.description");

            if (window.matchMedia("(min-width: 1579.99px)").matches) {
                if (itemWrapper) {
                    itemWrapper.style.transform = "translateY(0)";
                    itemWrapper.style.marginTop = "-221px"; // Поверніть на початкове значення
                }

                if (itemWrapperMiddle) {
                    itemWrapperMiddle.style.transform = "translateY(0)";
                    itemWrapperMiddle.style.marginTop = "-270px"; // Поверніть на початкове значення
                }

                if (itemWrapperSmall) {
                    itemWrapperSmall.style.transform = "translateY(0)";
                    itemWrapperSmall.style.marginTop = "-269px"; // Поверніть на початкове значення
                }
            } else {
                const mediaQuery1579 = window.matchMedia("(max-width: 1579.98px)");
                if (mediaQuery1579.matches) {
                    if (itemWrapper) {
                        itemWrapper.style.minHeight = "270px";
                        itemWrapper.style.marginTop = "-270px";
                        itemWrapper.style.transform = "translateY(0)";
                        itemWrapper.style.paddingLeft = "15px";
                    }
                    if (itemWrapperMiddle) {
                        itemWrapperMiddle.style.marginTop = "-270px";
                        itemWrapperMiddle.style.paddingLeft = "15px";
                        itemWrapperMiddle.style.transform = "translateY(0)";
                    }
                    if (itemWrapperSmall) {
                        itemWrapperSmall.style.marginTop = "-270px";
                        itemWrapperSmall.style.paddingLeft = "15px";
                        itemWrapperSmall.style.transform = "translateY(0)";
                    }
                }

                const mediaQuery1439 = window.matchMedia("(max-width: 1439.98px)");
                if (mediaQuery1439.matches) {
                    if (itemWrapper) {
                        itemWrapper.style.marginTop = "-269px";
                        itemWrapper.style.transform = "translateY(0)";
                    }
                    if (itemWrapperMiddle) {
                        itemWrapperMiddle.style.marginTop = "-269px";
                        itemWrapperMiddle.style.transform = "translateY(0)";
                    }
                    if (itemWrapperSmall) {
                        itemWrapperSmall.style.marginTop = "-269px";
                        itemWrapperSmall.style.transform = "translateY(0)";
                    }
                }

                const mediaQuery1299 = window.matchMedia("(max-width: 1299.98px)");
                if (mediaQuery1299.matches) {
                    if (itemWrapper) {
                        itemWrapper.style.marginTop = "-269px";
                    }
                    if (itemWrapperSmall) {
                        itemWrapperSmall.style.marginTop = "-269px";
                    }
                    if (itemWrapperMiddle) {
                        itemWrapperMiddle.style.marginTop = "-294px";
                    }
                }

                const mediaQuery1023 = window.matchMedia("(max-width: 1023.98px)");
                if (mediaQuery1023.matches) {
                    if (itemWrapper) {
                        itemWrapper.style.marginTop = "-269px";
                    }
                    if (itemWrapperMiddle) {
                        itemWrapperMiddle.style.marginTop = "-228px";
                    }
                    if (itemWrapperSmall) {
                        itemWrapperSmall.style.marginTop = "-269px";
                    }
                }

                const mediaQuery767 = window.matchMedia("(max-width: 767.98px)");
                if (mediaQuery767.matches) {
                    if (itemWrapper) {
                        itemWrapper.style.marginTop = "-270px";
                    }
                    if (itemWrapperMiddle) {
                        itemWrapperMiddle.style.marginTop = "-270px";
                    }
                    if (itemWrapperSmall) {
                        itemWrapperSmall.style.marginTop = "-200px";
                    }
                }

                const mediaQuery479 = window.matchMedia("(max-width: 479.98px)");
                if (mediaQuery479.matches) {
                    if (itemWrapper) {
                        itemWrapper.style.marginTop = "-187px";
                    }
                    if (itemWrapperMiddle) {
                        itemWrapperMiddle.style.marginTop = "-187px";
                    }
                    if (itemWrapperSmall) {
                        itemWrapperSmall.style.marginTop = "-187px";
                    }
                }
            }

            if (itemDescription) {
                itemDescription.style.opacity = "0";
            }

            activeItem = null;
        }
    });
});
