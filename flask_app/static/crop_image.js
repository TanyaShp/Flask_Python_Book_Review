const image = document.querySelector('#image');
const preview = document.querySelector('#preview');
const cropBtn = document.querySelector('#crop-btn');
const okBtn = document.querySelector('#ok-btn');
const cancelBtn = document.querySelector('#cancel-btn');
const croppedData = document.querySelector('#croppedData');
let imageCropped = false;
let croppedImageBlob;
let cropper;
var addForm = document.querySelector('#add-book-form');
var editForm = document.querySelector('#edit-book-form');

image.addEventListener('change', function (e) {
  const files = e.target.files;

  if (!files.length) {
    return;
  }

  let reader = new FileReader();

  reader.onload = function (e) {
    const img = new Image();
    img.onload = function () {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      let width = img.width;
      let height = img.height;

      canvas.width = width;
      canvas.height = height;
      ctx.drawImage(img, 0, 0, width, height);

      const resizedData = canvas.toDataURL();

      preview.src = resizedData;
      cropBtn.removeAttribute('disabled');
      preview.parentElement.style.display = ''; // show the preview container

      // Store the resized image data in the hidden field
      croppedData.value = resizedData;
    };
    img.src = e.target.result;
  };


  reader.readAsDataURL(files[0]);
  okBtn.style.display = '';
});

cropBtn.addEventListener('click', function () {
  if (cropper) {
    // Get the cropped image before destroying the Cropper instance
    const canvas = cropper.getCroppedCanvas();
    const croppedImage = canvas.toDataURL();

    // Destroy the Cropper instance
    cropper.destroy();
    cropper = null;

    // Set the cropped image to the preview
    preview.src = croppedImage;
    croppedData.value = croppedImage;

    preview.parentElement.style.display = ''; // show the preview container
    cancelBtn.removeAttribute('disabled'); // enable the cancel button
    cropBtn.style.display = 'none'; // hide the crop button

    // Enable the OK button
    okBtn.style.display = '';
    okBtn.removeAttribute('disabled');

  } else {
    // Initialize cropper with the preview image
    cropper = new Cropper(preview, {
      aspectRatio: NaN,
      viewMode: 1,
      autoCropArea: 1,
    });
    

    preview.parentElement.style.display = ''; // show the preview container
    cropBtn.setAttribute('disabled', 'disabled'); // disable the crop button
    cancelBtn.removeAttribute('disabled'); // enable the cancel button
    okBtn.style.display = '';
    okBtn.removeAttribute('disabled');
  }
});

okBtn.addEventListener('click', function () {
  // Hide the OK button
  okBtn.style.display = 'none';
  okBtn.setAttribute('disabled', 'disabled');
  // Generate a new blob for the cropped image and assign it to croppedImageBlob
  const canvas = cropper.getCroppedCanvas();
  canvas.toBlob(function (blob) {
    croppedImageBlob = blob;
  });

  if (cropper) {
    // Get the cropped image before destroying the Cropper instance
    const canvas = cropper.getCroppedCanvas();
    const croppedImage = canvas.toDataURL();

    // Destroy the Cropper instance
    cropper.destroy();
    cropper = null;

    // Set the cropped image to the preview
    preview.src = croppedImage;
  }

  // Enable the Crop button
  cropBtn.removeAttribute('disabled');
  cropBtn.style.display = '';

  // Disable the Cancel button
  cancelBtn.setAttribute('disabled', 'disabled');
});


cancelBtn.addEventListener('click', function () {
  if (cropper) {
    cropper.destroy();
    cropper = null;
  }

  preview.src = croppedData.value || preview.src; // display the cropped image or original image
  preview.parentElement.style.display = ''; // show the preview container
  this.setAttribute('disabled', 'disabled'); // disable the cancel button
  cropBtn.removeAttribute('disabled'); // enable the crop button
  cropBtn.style.display = '';
  okBtn.style.display = 'none'; // hide the OK button
  okBtn.setAttribute('disabled', 'disabled'); // disable the OK button
});

image.addEventListener('click', function () {
  // Reset buttons to their initial state
  cropBtn.style.display = '';
  okBtn.style.display = 'none';
  cancelBtn.setAttribute('disabled', 'disabled');

  // Reset the preview image
  preview.src = '';
});

function handleFormSubmission(formElement, submitUrl) {
  formElement.addEventListener('submit', function (event) {
    event.preventDefault();

    let formData = new FormData(this);

    if (croppedImageBlob) {
      formData.append('cropped_image', croppedImageBlob, 'cropped_image.png');
    } else if (image.files.length > 0) {
      formData.append('original_image', image.files[0], image.files[0].name);
    }

    submitFormData(formData, submitUrl, formElement);
  });
}


function submitFormData(formData, submitUrl, formElement) {
  fetch(submitUrl, {
    method: 'POST',
    body: formData,
  })
    .then(response => response.json())
    .then(result => {
      console.log(result);
      if (result.location) {
        window.location.href = result.location;
      }
    })
    .catch(error => {
      console.error('Error:', error);
    })
    .finally(() => {
      // Reset the form submission
      formData = new FormData();
      formElement.reset();
    });
}

if (addForm) {
  handleFormSubmission(addForm, addBookUrl);
} else if (editForm) {
  handleFormSubmission(editForm, editBookUrl);
}

