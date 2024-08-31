document.addEventListener('DOMContentLoaded', function () {
    let deleteStockId = null;

    console.log('DOM loaded successfully...in Stock');
    
    // Delete button click event to show confirmation modal
    document.querySelectorAll('.delete-btn3').forEach(function (button) {
        console.log('Stock log-----------delete')
        button.addEventListener('click', function () {
            deleteStockId = this.dataset.id;
            var deleteModal = new bootstrap.Modal(document.getElementById('deleteModalStock'));
            deleteModal.show();
        });
    });

    // Confirm delete button click event
    // document.getElementById('confirmDeleteStock').addEventListener('click', function () {
    //     if (deleteStockId) {
    //         fetch('/stock/' + deleteStockId, {
    //             method: 'DELETE',
    //             headers: {
    //                 'Content-Type': 'application/json'
    //             }
    //         }).then(response => {
    //             if (response.status === 200) {
    //                 showPopup('Deleted', 'This stock record has been deleted successfully.');
    //                 setTimeout(() => {
    //                     window.location.href = window.location.origin + '/stocks';
    //                 }, 2000);
    //             } else {
    //                 showPopup('Error', 'Failed to delete stock.');
    //             }
    //             var deleteModal = bootstrap.Modal.getInstance(document.getElementById('deleteModalStock'));
    //             deleteModal.hide();
    //         }).catch(error => {
    //             console.error('Error:', error);
    //             alert('An error occurred while deleting the stock.');
    //         });
    //     }
    // });

    // Edit button click event to show the edit modal
    // let editStockId = null;
    // document.querySelectorAll('.edit-btn3').forEach(function (button) {
    //     button.addEventListener('click', function () {
    //         console.log('Clicked edit button for Stock');
    //         editStockId = this.dataset.id;

    //         // Fetch the stock details by ID and populate the form in the modal
    //         fetch('/stock/' + editStockId)
    //             .then(response => {
    //                 if (!response.ok) {
    //                     throw new Error('Network response was not ok');
    //                 }
    //                 return response.json();
    //             })
    //             .then(data => {
    //                 console.log('Fetched stock data:', data);

    //                 // Populate the form with the stock data
    //                 document.getElementById('stockId').value = data.id;
    //                 document.getElementById('productName').value = data.name;
    //                 document.getElementById('productQuantity').value = data.product_quantity;
    //                 document.getElementById('lastUpdateDate').value = new Date(data.last_update_date).toISOString().slice(0, 10);

    //                 // Show the modal
    //                 var editModal = new bootstrap.Modal(document.getElementById('editStockModal'));
    //                 editModal.show();
    //             })
    //             .catch(error => {
    //                 console.error('Error fetching stock data:', error);
    //                 alert('An error occurred while fetching the stock data.');
    //             });
    //     });
    // });

    // Form submission for updating the stock
    // document.getElementById('editStockForm').addEventListener('submit', function (e) {
    //     e.preventDefault();
    //     console.log('Submitting update for Stock ID:', editStockId);

    //     const formData = new FormData(this);
    //     const formJSON = JSON.stringify(Object.fromEntries(formData.entries()));

    //     fetch('/stock/' + editStockId, {
    //         method: 'PUT',
    //         headers: {
    //             'Content-Type': 'application/json'
    //         },
    //         body: formJSON
    //     }).then(response => response.json().then(data => ({ status: response.status, body: data })))
    //         .then(({ status, body }) => {
    //             if (status === 200) {
    //                 window.location.reload(); // Reload the page to show updated data
    //             } else {
    //                 alert('An error occurred while updating the stock.');
    //             }
    //         }).catch(error => {
    //             console.error('Error:', error);
    //             alert('An error occurred while updating the stock.');
    //         });

    // });

    // Filter stock
    console.log('in stock....93');
    const filterStockInput = document.getElementById('filter_stock');
    const stockTableBody = document.getElementById('stockTableBody');
    console.log('constants-->', filterStockInput, stockTableBody);

    filterStockInput.addEventListener('input', function () {
        const query = this.value;
        console.log('Inside filter stock');

        // Send a request to the server to get the filtered stock
        fetch(`/stock/filter?query=${query}`)
            .then(response => response.json())
            .then(data => {
                // Clear the current table rows
                stockTableBody.innerHTML = '';

                // Populate the table with the filtered stock
                console.log('data-->', data);
                data.stocks.forEach(stock => {
                    const row = `
                    <tr id="stock-${stock.id}">
                        <td>${stock.id}</td>
                        <td>${stock.name}</td>
                        <td>${stock.product_quantity}</td>
                        <td>${new Date(stock.last_update_date).toISOString().slice(0, 10)}</td>
                        <td>
                            <button class="btn btn-warning btn-sm edit-btn3" data-id="${stock.id}">Edit</button>
                            <button class="btn btn-danger btn-sm delete-btn3" data-id="${stock.id}">Delete</button>
                        </td>
                    </tr>
                `;
                    stockTableBody.insertAdjacentHTML('beforeend', row);
                });
            })
            .catch(error => console.error('Error fetching filtered stock:', error));
    });

    // Show add stock modal
    console.log('Stock add.............')
    document.getElementById('add_stock').addEventListener('click', function () {
        console.log('click add stock button');
        var addStockModal = new bootstrap.Modal(document.getElementById('addStockModal'));
        addStockModal.show();
    });

    // Handle form submission for adding a stock
    document.getElementById('addStockForm').addEventListener('submit', function (e) {
        e.preventDefault();
        console.log('addStockModel:: POST call 1111');

        const formData = new FormData(this);
        // Convert FormData to a plain object
        const formObject = Object.fromEntries(formData.entries());
        const formJSON = JSON.stringify(formObject);

        console.log('addStockModel:: POST call', formJSON);
        fetch('/stock', {
            method: 'POST',
            body: formData
        }).then(response => response.json().then(data => ({ status: response.status, body: data })))
            .then(({ status, body }) => {
                console.error('Status:', status);
                const modalElement = document.getElementById('addStockModal');
                const modal = bootstrap.Modal.getInstance(modalElement); // Get the modal instance
                if (status === 201) {  // Check for the 201 Created status code
                    modal.hide(); // Hide the modal
                    document.getElementById('addStockForm').reset(); // Reset the form
                    showPopup('Success', 'Stock record inserted successfully!');
                    setTimeout(() => {
                        window.location.reload(); // Reload to reflect the new stock
                    }, 2000);
                }
                else if (status === 404) {
                    showPopup('Error', body.message || 'Product not found in Product table!');
                    modal.hide();
                    setTimeout(() => {
                        window.location.reload(); // Reload to reflect the new stock
                    }, 3000);

                }
                else {
                    showPopup('Error', body.message || 'Failed to insert stock record.');
                    modal.hide();
                    setTimeout(() => {
                        window.location.reload(); // Reload to reflect the new stock
                    }, 3000);

                }
            }).catch(error => {
                console.error('Error:', error);
                showPopup('Error', 'An error occurred while inserting the stock record.');
            });
    });
});
