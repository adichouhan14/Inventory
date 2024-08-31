document.addEventListener('DOMContentLoaded', function () {
    let deletePurchaseId = null;

    console.log('DOM loaded successfully...in Purchases');
    // Delete button click event to show confirmation modal
    document.querySelectorAll('.delete-btn2').forEach(function (button) {
        console.log('Purchase log-----------delete');
        button.addEventListener('click', function () {
            deletePurchaseId = this.dataset.id;
            var deleteModal = new bootstrap.Modal(document.getElementById('deleteModalPurchase'));
            deleteModal.show();
        });
    });

    // Confirm delete button click event
    document.getElementById('confirmDeletePurchase').addEventListener('click', function () {
        if (deletePurchaseId) {
            fetch('/purchase/' + deletePurchaseId, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(response => {
                if (response.status === 200) {
                    showPopup('Deleted', 'This purchase record has been deleted successfully.');
                    setTimeout(() => {
                        window.location.href = window.location.origin + '/purchases';
                    }, 2000);
                } else {
                    showPopup('Error', 'Failed to delete purchase.');
                }
                var deleteModal = bootstrap.Modal.getInstance(document.getElementById('deleteModalPurchase'));
                deleteModal.hide();
            }).catch(error => {
                console.error('Error:', error);
                alert('An error occurred while deleting the purchase.');
            });
        }
    });

    // Edit button click event to show the edit modal
    let editPurchaseId = null;
    document.querySelectorAll('.edit-btn2').forEach(function (button) {
        button.addEventListener('click', function () {
            console.log('Clicked edit button for Purchase');
            editPurchaseId = this.dataset.id;
            console.log('editPurchaseId-->',editPurchaseId)
            // Fetch the purchase details by ID and populate the form in the modal
            fetch('/purchase/' + editPurchaseId)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Fetched purchase data:', data);

                    // Populate the form with the purchase data
                    document.getElementById('purchaseId').value = data.id;
                    document.getElementById('productName').value = data.name;
                    document.getElementById('purchaseQuantity').value = data.purchase_quantity;
                    document.getElementById('purchaseRate').value = data.purchase_rate;
                    document.getElementById('purchaseAmount').value = data.purchase_amount;

                    // Show the modal
                    var editModal = new bootstrap.Modal(document.getElementById('editPurchaseModal'));
                    editModal.show();
                })
                .catch(error => {
                    console.error('Error fetching purchase data:', error);
                    alert('An error occurred while fetching the purchase data.');
                });
        });
    });

    // Form submission for updating the purchase
    document.getElementById('editPurchaseForm').addEventListener('submit', function (e) {
        e.preventDefault();
        console.log('Submitting update for Purchase ID:', editPurchaseId);

        const formData = new FormData(this);
        const formJSON = JSON.stringify(Object.fromEntries(formData.entries()));

        fetch('/purchase/' + editPurchaseId, {
            method: 'PUT',  // Ensure this is set to PUT
            headers: {
                'Content-Type': 'application/json'
            },
            body: formJSON
        }).then(response => response.json().then(data => ({ status: response.status, body: data })))
            .then(({ status, body }) => {
                if (status === 200) {
                    window.location.reload(); // Reload the page to show updated data
                } else {
                    alert('An error occurred while updating the purchase.');
                }
            }).catch(error => {
                console.error('Error:', error);
                alert('An error occurred while updating the purchase.');
            });

    });

    // Filter
    console.log('in purchases....93');
    const filterPurchaseInput = document.getElementById('filter_purchase');
    const purchaseTableBody = document.getElementById('purchaseTableBody');
    console.log('constants-->', filterPurchaseInput, purchaseTableBody);
    filterPurchaseInput.addEventListener('input', function () {
        const query = this.value;
        console.log('Inside filter purchases');
        // Send a request to the server to get the filtered purchases
        fetch(`/purchase/filter?query=${query}`)
            .then(response => response.json())
            .then(data => {
                // Clear the current table rows
                purchaseTableBody.innerHTML = '';

                // Populate the table with the filtered purchases
                console.log('data-->', data);
                data.purchases.forEach(purchase => {
                    const row = `
                        <tr id="purchase-${purchase.id}">
                            <td>${purchase.id}</td>
                            <td>${purchase.name}</td>
                            <td>${purchase.purchase_quantity}</td>
                            <td>${purchase.purchase_rate}</td>
                            <td>${purchase.purchase_amount}</td>
                            <td>${new Date(purchase.purchase_date).toISOString().slice(0, 10)}</td>
                            <td>
                                <button class="btn btn-warning btn-sm edit-btn2" data-id="${purchase.id}">Edit</button>
                                <button class="btn btn-danger btn-sm delete-btn2" data-id="${purchase.id}">Delete</button>
                            </td>
                        </tr>
                    `;
                    purchaseTableBody.insertAdjacentHTML('beforeend', row);
                });
            })
            .catch(error => console.error('Error fetching filtered purchases:', error));
    });

    // Show add purchase modal
    console.log('Purchases add.............');
    document.getElementById('add_purchase').addEventListener('click', function () {
        console.log('click add purchase button');
        var addPurchaseModal = new bootstrap.Modal(document.getElementById('addPurchaseModal'));
        addPurchaseModal.show();
    });

    // Handle form submission for adding a purchase
    document.getElementById('addPurchaseForm').addEventListener('submit', function (e) {
        e.preventDefault();
        console.log('addPurchaseModel:: POST call 1111');

        const formData = new FormData(this);
        // Convert FormData to a plain object
        const formObject = Object.fromEntries(formData.entries());
        const formJSON = JSON.stringify(formObject);

        console.log('addPurchaseModel:: POST call', formJSON);
        fetch('/purchase', {
            method: 'POST',
            body: formData
        }).then(response => response.json().then(data => ({ status: response.status, body: data })))
            .then(({ status, body }) => {
                console.error('Status:', status);
                const modalElement = document.getElementById('addPurchaseModal');
                const modal = bootstrap.Modal.getInstance(modalElement); // Get the modal instance
                if (status === 201) {  // Check for the 201 Created status code
                    modal.hide(); // Hide the modal
                    document.getElementById('addPurchaseForm').reset(); // Reset the form
                    showPopup('Success', 'Purchase record inserted successfully!');
                    setTimeout(() => {
                        window.location.reload(); // Reload to reflect the new purchase
                    }, 2000);
                } 
                else if (status === 404) { 
                    showPopup('Error', body.message || 'Product not found in Product table!');
                    modal.hide(); 
                }
                else {
                    showPopup('Error', body.message || 'Failed to insert purchase.');
                    modal.hide();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while adding the purchase.');
            });
    });
});

