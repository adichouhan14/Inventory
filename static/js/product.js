document.addEventListener('DOMContentLoaded', function () {
    let deleteProductId = null;

    console.log('DOM loaded successfully...');
    // Delete button click event to show confirmation modal
    document.querySelectorAll('.delete-btn').forEach(function (button) {
        button.addEventListener('click', function () {
            console.log('click delete button Product');
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
                    showPopup('Deleted', 'The product has been deleted successfully.');
                    setTimeout(() => {
                        window.location.href = window.location.origin + '/products';
                    }, 2000);
                } else {
                    showPopup('Error', 'Failed to delete product.');
                }
                var deleteModal = bootstrap.Modal.getInstance(document.getElementById('deleteModal'));
                deleteModal.hide();
            }).catch(error => {
                console.error('Error:', error);
                alert('An error occurred while deleting the product.');
            });
        }
    });


    // Edit button click event to show the edit modal
    let editProductId = null;
    document.querySelectorAll('.edit-btn').forEach(function (button) {
        button.addEventListener('click', function () {
            console.log('click edit button');
            editProductId = this.dataset.id;
            // console.log('Product id ::', editProductId);
            fetch('/product/' + editProductId)
                .then(response => response.json())
                .then(data => {
                    console.log('data:::', data);
                    // Populate the form with the product data
                    document.getElementById('recordId').value = data.id;
                    document.getElementById('recordName').value = data.name;
                    document.getElementById('recordCategory').value = data.category;
                    // Show the modal
                    // console.log('document.getElementById:::', document.getElementById('category'));
                    var editModal = new bootstrap.Modal(document.getElementById('editModal'));
                    // console.log('editModel:::', editModal);
                    editModal.show();
                });
        });
    });


    // Form submission for update
    document.getElementById('editForm').addEventListener('submit', function (e) {
        e.preventDefault();
        console.log('editModel:: Update calll 1111');
        const formData = new FormData(this);
        const formJSON = JSON.stringify(Object.fromEntries(formData));
        console.log('editModel:: Update calll');
        fetch('/product/' + editProductId, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: formJSON
        }).then(response => response.json().then(data => ({ status: response.status, body: data })))
            .then(({ status, body }) => {
                console.error('Status update:', status);
                if (status === 200) {
                    window.location.reload(); // Reload the page to show updated data
                } else {
                    alert('An error occurred while updating the product.');
                }
            }).catch(error => {
                console.error('Error:', error);
                alert('An error occurred while updating the product.');
            });
    });


    const filterInput = document.getElementById('filter_product');
    const productTableBody = document.getElementById('productTableBody');

    filterInput.addEventListener('input', function () {
        const query = this.value;

        // Send a request to the server to get the filtered products
        fetch(`/product/filter?query=${query}`)
            .then(response => response.json())
            .then(data => {
                // Clear the current table rows
                productTableBody.innerHTML = '';

                // Populate the table with the filtered products
                data.products.forEach(product => {
                    const row = `
                        <tr id="product-${product.id}">
                            <td>${product.id}</td>
                            <td>${product.category}</td>
                            <td>${product.name}</td>
                            <td>${new Date(product.introduce_date).toISOString().slice(0, 10)}</td>
                            <td>
                                <button class="btn btn-warning btn-sm edit-btn" data-id="${product.id}">Edit</button>
                                <button class="btn btn-danger btn-sm delete-btn" data-id="${product.id}">Delete</button>
                            </td>
                        </tr>
                    `;
                    productTableBody.insertAdjacentHTML('beforeend', row);
                });
            })
            .catch(error => console.error('Error fetching filtered products:', error));
    });

    document.getElementById('add_product').addEventListener('click', function () {
        console.log('click add button');
        var addModal = new bootstrap.Modal(document.getElementById('addModal'));
        addModal.show();

    });

    document.getElementById('addForm').addEventListener('submit', function (e) {
        e.preventDefault();
        console.log('addModel:: add call 1111');

        const formData = new FormData(this);
        // Convert FormData to a plain object
        const formObject = Object.fromEntries(formData.entries());
        const formJSON = JSON.stringify(formObject);

        console.log('addModel:: POST call', formJSON);
        fetch('/product', {
            method: 'POST',
            body: formData
        }).then(response => response.json().then(data => ({ status: response.status, body: data })))
            .then(({ status, body }) => {
                console.error('Status:', status);
                if (status === 201) {  // Check for the 201 Created status code
                    // document.getElementById('addModal').hide()
                    const modalElement = document.getElementById('addModal');
                    const modal = bootstrap.Modal.getInstance(modalElement); // Get the modal instance
                    modal.hide(); // Hide the modal
                    document.getElementById('addForm').reset(); // Reset the form
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
});

