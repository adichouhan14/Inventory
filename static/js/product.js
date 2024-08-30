document.addEventListener('DOMContentLoaded', function () {
    let deleteProductId = null;

    // Delete button click event to show confirmation modal
    document.querySelectorAll('.delete-btn').forEach(function (button) {
        button.addEventListener('click', function () {
            deleteProductId = this.dataset.id;
            var deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
            deleteModal.show();
        });
    });

    // Confirm delete button click event
    document.getElementById('confirmDelete').addEventListener('click', function () {
        if (deleteProductId) {
            fetch('/product/' + deleteProductId, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(response => {
                console.log('Response status:', response.status);
                console.log('Response status:', response.status);
                console.log('Response status:', response.status);
                if (response.status === 200) {  // Assuming response.ok checks for a successful status code
                    console.log('Response status: insidddddddddddddddddddddddddeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee');
                    // alert('Product deleted.');
                    showPopup('Deleted', 'The product has been deleted successfully.');
                    setTimeout(() => {
                        window.location.href = window.location.origin + '/products';
                    }, 2000);
                    // window.location.href = window.location.origin + '/products'; // Redirect to product page after showing popup
                } else {
                    showPopup('Error', 'Failed to delete product.');
                }
                
                // if (response.status === 200) {
                //     window.location.href = window.location.origin + '/products'; // Redirect to the products page dynamically
                // } else {
                //     alert('Failed to delete product.');
                // }

                var deleteModal = bootstrap.Modal.getInstance(document.getElementById('deleteModal'));
                deleteModal.hide();
            }).catch(error => {
                console.error('Error:', error);
                alert('An error occurred while deleting the product.');
            });
        }
    });
});

document.getElementById('addProductForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);

    fetch('/product', {
        method: 'POST',
        body: formData
    }).then(response => response.json().then(data => ({ status: response.status, body: data })))
    .then(({ status, body }) => {
        console.error('Status:', status);
        if (status === 201) {  // Check for the 201 Created status code
            console.error('')
            showPopup('Success', 'Product inserted successfully!');
            setTimeout(() => {
                window.location.href = window.location.origin + '/products';
            }, 2000);
        } else {
            showPopup('Error', body.message || 'Failed to insert product.');
            window.location.href = window.location.origin + '/products';
        }
    }).catch(error => {
        console.error('Error:', error);
        showPopup('Error', 'An error occurred while inserting the product.'); 
    });
});
