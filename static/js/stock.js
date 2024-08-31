document.addEventListener('DOMContentLoaded', function () {
    let deleteSalesId = null;

    console.log('DOM loaded successfully...in Sales');
    // Delete button click event to show confirmation modal
    document.querySelectorAll('.delete-btn1').forEach(function (button) {
        console.log('Sales log-----------delete')
        button.addEventListener('click', function () {
            deleteSalesId = this.dataset.id;
            var deleteModal = new bootstrap.Modal(document.getElementById('deleteModalSales'));
            deleteModal.show();
        });
    });

    // Confirm delete button click event
    document.getElementById('confirmDeleteSales').addEventListener('click', function () {
        if (deleteSalesId) {
            fetch('/sale/' + deleteSalesId, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(response => {
                if (response.status === 200) {  // Assuming response.ok checks for a successful status code
                    showPopup('Deleted', 'This sale record has been deleted successfully.');
                    setTimeout(() => {
                        window.location.href = window.location.origin + '/sales';
                    }, 2000);
                } else {
                    showPopup('Error', 'Failed to delete sales.');
                }
                var deleteModal = bootstrap.Modal.getInstance(document.getElementById('deleteModalSales'));
                deleteModal.hide();
            }).catch(error => {
                console.error('Error:', error);
                alert('An error occurred while deleting the sales.');
            });
        }
    });

    // Edit button click event to show the edit modal
    let editSalesId = null;
    document.querySelectorAll('.edit-btn1').forEach(function (button) {
        button.addEventListener('click', function () {
            console.log('Clicked edit button for Sales');
            editSalesId = this.dataset.id;

            // Fetch the sale details by ID and populate the form in the modal
            fetch('/sale/' + editSalesId)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Fetched sale data:', data);

                    // Populate the form with the sale data
                    document.getElementById('saleId').value = data.id;
                    document.getElementById('productName').value = data.name;
                    document.getElementById('salesQuantity').value = data.sales_quantity;
                    document.getElementById('salesRate').value = data.sales_rate;
                    document.getElementById('salesAmount').value = data.sales_amount;

                    // Show the modal
                    var editModal = new bootstrap.Modal(document.getElementById('editSalesModal'));
                    editModal.show();
                })
                .catch(error => {
                    console.error('Error fetching sale data:', error);
                    alert('An error occurred while fetching the sale data.');
                });
        });
    });

    // Form submission for updating the sale
    document.getElementById('editSalesForm').addEventListener('submit', function (e) {
        e.preventDefault();
        console.log('Submitting update for Sale ID:', editSalesId);

        const formData = new FormData(this);
        const formJSON = JSON.stringify(Object.fromEntries(formData.entries()));

        fetch('/sale/' + editSalesId, {
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
                    alert('An error occurred while updating the sale.');
                }
            }).catch(error => {
                console.error('Error:', error);
                alert('An error occurred while updating the sale.');
            });

    });

    //Filter
    console.log('in sales....93')
    const filterSalesInput = document.getElementById('filter_sale');
    const salesTableBody = document.getElementById('salesTableBody');
    console.log('constants-->', filterSalesInput, salesTableBody)
    filterSalesInput.addEventListener('input', function () {
        const query = this.value;
        console.log('Inside filter sales')
        // Send a request to the server to get the filtered products
        fetch(`/sale/filter?query=${query}`)
            .then(response => response.json())
            .then(data => {
                // Clear the current table rows
                salesTableBody.innerHTML = '';

                // Populate the table with the filtered products
                console.log('data-->', data)
                data.sales.forEach(sale => {
                    const row = `
                        <tr id="sale-${sale.id}">
                            <td>${sale.id}</td>
                            <td>${sale.name}</td>
                            <td>${sale.sales_quantity}</td>
                            <td>${sale.sales_rate}</td>
                            <td>${sale.sales_amount}</td>
                            <td>${new Date(sale.sales_date).toISOString().slice(0, 10)}</td>
                            <td>
                                <button class="btn btn-warning btn-sm edit-btn1" data-id="${sale.id}">Edit</button>
                                <button class="btn btn-danger btn-sm delete-btn1" data-id="${sale.id}">Delete</button>
                            </td>
                        </tr>
                    `;
                    salesTableBody.insertAdjacentHTML('beforeend', row);
                });
            })
            .catch(error => console.error('Error fetching filtered sales:', error));
    });

    // Show add sales modal
    console.log('Sales add.............')
    document.getElementById('add_sale').addEventListener('click', function () {
        console.log('click add sale button');
        var addSalesModal = new bootstrap.Modal(document.getElementById('addSalesModal'));
        addSalesModal.show();
    });

    // Handle form submission for adding a sale
    document.getElementById('addSalesForm').addEventListener('submit', function (e) {
        e.preventDefault();
        console.log('addSalesModel:: POST call 1111');

        const formData = new FormData(this);
        // Convert FormData to a plain object
        const formObject = Object.fromEntries(formData.entries());
        const formJSON = JSON.stringify(formObject);

        console.log('addSalesModel:: POST call', formJSON);
        fetch('/sale', {
            method: 'POST',
            body: formData
        }).then(response => response.json().then(data => ({ status: response.status, body: data })))
            .then(({ status, body }) => {
                console.error('Status:', status);
                const modalElement = document.getElementById('addSalesModal');
                const modal = bootstrap.Modal.getInstance(modalElement); // Get the modal instance
                if (status === 201) {  // Check for the 201 Created status code
                    modal.hide(); // Hide the modal
                    document.getElementById('addSalesForm').reset(); // Reset the form
                    showPopup('Success', 'Sale record inserted successfully!');
                    setTimeout(() => {
                        window.location.reload(); // Reload to reflect the new sale
                    }, 2000);
                } 
                else if (status === 404) { 
                    showPopup('Error', body.message || 'Product not found in Product table!');
                    modal.hide();
                    setTimeout(() => {
                        window.location.reload(); // Reload to reflect the new sale
                    }, 3000);
                    
                }
                else {
                    showPopup('Error', body.message || 'Failed to insert sale record.');
                    modal.hide();
                    setTimeout(() => {
                        window.location.reload(); // Reload to reflect the new sale
                    }, 3000);
                    
                }
            }).catch(error => {
                console.error('Error:', error);
                showPopup('Error', 'An error occurred while inserting the sale record.');
            });
    });
});
