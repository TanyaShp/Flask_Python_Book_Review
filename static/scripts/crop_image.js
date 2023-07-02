// select the relevant HTML elements by their ids
const image = document.querySelector('#image');
const preview = document.querySelector('#preview');
const cropBtn = document.querySelector('#crop-btn');
const okBtn = document.querySelector('#ok-btn');
const cancelBtn = document.querySelector('#cancel-btn');
const croppedData = document.querySelector('#croppedData');

// initialize necessary variables
let imageCropped = false;
let croppedImageBlob;
let cropper;
var addForm = document.querySelector('#add-book-form');
var editForm = document.querySelector('#edit-book-form');

// event listener for when a new image is selected for uploading
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

      // store the resized image data in the hidden field
      croppedData.value = resizedData;
    };
    img.src = e.target.result;
  };

  // reads in the selected image file as a data URL
  reader.readAsDataURL(files[0]);
  okBtn.style.display = '';
});

// if the previous image was being edited, initialize the crop button
window.onload = function () {
  if (preview.src) {
    cropBtn.removeAttribute('disabled');
  }
};

// listener for the crop button, creates a new instance of Cropper.js on the preview image
cropBtn.addEventListener('click', function () {
  if (cropper) {
    // get the cropped image before destroying the Cropper instance
    const canvas = cropper.getCroppedCanvas();
    const croppedImage = canvas.toDataURL();

    // destroy the Cropper instance
    cropper.destroy();
    cropper = null;

    // set the cropped image to the preview
    preview.src = croppedImage;
    croppedData.value = croppedImage;

    preview.parentElement.style.display = ''; // show the preview container
    cancelBtn.removeAttribute('disabled'); // enable the cancel button
    cropBtn.style.display = 'none'; // hide the crop button

    // enable the OK button
    okBtn.style.display = '';
    okBtn.removeAttribute('disabled');

  } else {
    // initialize cropper with the preview image
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

// listener for the ok button, finalizes the cropping process and hides the button
okBtn.addEventListener('click', function () {
  // hide the OK button
  okBtn.style.display = 'none';
  okBtn.setAttribute('disabled', 'disabled');
  // generate a new blob for the cropped image and assign it to croppedImageBlob
  const canvas = cropper.getCroppedCanvas();
  canvas.toBlob(function (blob) {
    croppedImageBlob = blob;
  });

  if (cropper) {
    // get the cropped image before destroying the Cropper instance
    const canvas = cropper.getCroppedCanvas();
    const croppedImage = canvas.toDataURL();

    // destroy the Cropper instance
    cropper.destroy();
    cropper = null;

    // set the cropped image to the preview
    preview.src = croppedImage;
  }

  // enable the Crop button
  cropBtn.removeAttribute('disabled');
  cropBtn.style.display = '';

  // disable the Cancel button
  cancelBtn.setAttribute('disabled', 'disabled');
});

// listener for the cancel button, destroys the Cropper.js instance and resets the preview image
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

// listener for clicking on the image, resets the crop and ok buttons and the preview image
image.addEventListener('click', function () {
  // reset buttons to their initial state
  cropBtn.style.display = '';
  okBtn.style.display = 'none';
  cancelBtn.setAttribute('disabled', 'disabled');

  // reset the preview image
  preview.src = '';
});

// handle the form submission, adds the cropped image or the original image to the form data
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

// submit the form data to the server
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

// handle the form submission depending on whether the add book form or the edit book form is present
if (addForm) {
  handleFormSubmission(addForm, addBookUrl);
} else if (editForm) {
  handleFormSubmission(editForm, editBookUrl);
}

