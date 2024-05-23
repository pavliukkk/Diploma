function selectPhoto() {
    document.getElementById('fileInput').click();
}

function submitForm(event) {
    if (event) {
        event.preventDefault();
        document.getElementById('photoForm').submit();
    }
}
function displaySelectedPhoto(event) {
var fileInput = event.target;
var profileImage = document.getElementById('profileImage');
var reader = new FileReader();

reader.onload = function() {
  profileImage.src = reader.result;
};

reader.readAsDataURL(fileInput.files[0]);
}