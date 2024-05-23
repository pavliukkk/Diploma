async function getData() {
  const requestURL = 'https://pavliukkk.github.io/Kyrsova/features.json';
  try {
      const response = await fetch(requestURL);
      const services = await response.json();
      const shuffledServices = shuffleArray(services);
      populateService(shuffledServices);
  } catch (error) {
      console.error('Error fetching data:', error);
  }
}

function populateService(obj) {
   const serviceList = document.querySelector('.feature');

  obj.forEach(service => {
    const serviceElement = document.createElement('div');
    serviceElement.className = 'feature__item';

    const serviceImgDiv = document.createElement('div');
    serviceImgDiv.className = 'feature__item-img';
    const serviceImage = document.createElement('img');
    serviceImage.src = service.image;
    serviceImage.alt = service.title;
    serviceImgDiv.appendChild(serviceImage);

    const serviceTitle = document.createElement('div');
    serviceTitle.className = 'feature__item-title subtitle';
    serviceTitle.textContent = service.title;

    const serviceText = document.createElement('div');
    serviceText.className = 'text';
    serviceText.textContent = service.subtitle;

    serviceElement.appendChild(serviceImgDiv);
    serviceElement.appendChild(serviceTitle);
    serviceElement.appendChild(serviceText);

    serviceList.appendChild(serviceElement);
  });
}

function shuffleArray(array) {
  const shuffledArray = array.slice();
  for (let i = shuffledArray.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffledArray[i], shuffledArray[j]] = [shuffledArray[j], shuffledArray[i]];
  }
  return shuffledArray;
}

getData();